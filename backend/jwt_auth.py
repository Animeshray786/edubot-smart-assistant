"""
JWT Authentication Module
JSON Web Token based authentication system
"""

import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
from flask import request, jsonify, current_app
from database.db_manager import DatabaseManager

class JWTAuth:
    """JWT Authentication manager"""
    
    # Token expiration times
    ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRY = timedelta(days=30)
    
    # Blacklisted tokens (in production, use Redis)
    _blacklist = set()
    
    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize JWT Auth
        
        Args:
            secret_key: Secret key for signing tokens
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = 'HS256'
    
    def generate_access_token(self, user_id: int, username: str, 
                            role: str = 'user') -> str:
        """
        Generate JWT access token
        
        Args:
            user_id: User ID
            username: Username
            role: User role
            
        Returns:
            str: JWT access token
        """
        now = datetime.utcnow()
        payload = {
            'user_id': user_id,
            'username': username,
            'role': role,
            'type': 'access',
            'iat': now,
            'exp': now + self.ACCESS_TOKEN_EXPIRY,
            'jti': secrets.token_urlsafe(16)  # Unique token ID
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def generate_refresh_token(self, user_id: int) -> str:
        """
        Generate JWT refresh token
        
        Args:
            user_id: User ID
            
        Returns:
            str: JWT refresh token
        """
        now = datetime.utcnow()
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': now,
            'exp': now + self.REFRESH_TOKEN_EXPIRY,
            'jti': secrets.token_urlsafe(16)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def verify_token(self, token: str, 
                    token_type: str = 'access') -> Dict[str, Any]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            token_type: Expected token type ('access' or 'refresh')
            
        Returns:
            dict: Decoded token payload
            
        Raises:
            jwt.InvalidTokenError: If token is invalid
        """
        try:
            # Decode token
            payload = jwt.decode(
                token, 
                self.secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Check token type
            if payload.get('type') != token_type:
                raise jwt.InvalidTokenError(f'Invalid token type. Expected {token_type}')
            
            # Check if token is blacklisted
            jti = payload.get('jti')
            if jti and jti in self._blacklist:
                raise jwt.InvalidTokenError('Token has been revoked')
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise jwt.InvalidTokenError('Token has expired')
        except jwt.InvalidTokenError as e:
            raise e
        except Exception as e:
            raise jwt.InvalidTokenError(f'Token verification failed: {str(e)}')
    
    def revoke_token(self, token: str) -> bool:
        """
        Revoke a token (add to blacklist)
        
        Args:
            token: Token to revoke
            
        Returns:
            bool: True if successful
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_exp': False}  # Allow expired tokens to be revoked
            )
            
            jti = payload.get('jti')
            if jti:
                self._blacklist.add(jti)
                return True
            
            return False
            
        except Exception:
            return False
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """
        Generate new access token from refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            str: New access token or None if refresh token invalid
        """
        try:
            payload = self.verify_token(refresh_token, token_type='refresh')
            
            # Get user info from database
            db = DatabaseManager()
            user = db.get_user_by_id(payload['user_id'])
            
            if not user or not user.get('is_active'):
                return None
            
            # Generate new access token
            return self.generate_access_token(
                user['user_id'],
                user['username'],
                user['role']
            )
            
        except Exception:
            return None


# Decorator for protecting routes with JWT
def jwt_required(f):
    """
    Decorator to require JWT authentication
    Usage: @jwt_required
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        try:
            # Extract token (format: "Bearer <token>")
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'error': 'Invalid authorization header format'}), 401
            
            token = parts[1]
            
            # Get JWT auth instance from app
            jwt_auth = getattr(current_app, 'jwt_auth', None)
            if not jwt_auth:
                return jsonify({'error': 'JWT authentication not configured'}), 500
            
            # Verify token
            payload = jwt_auth.verify_token(token)
            
            # Add user info to request context
            request.user_id = payload['user_id']
            request.username = payload['username']
            request.user_role = payload['role']
            
            return f(*args, **kwargs)
            
        except jwt.InvalidTokenError as e:
            return jsonify({'error': f'Invalid token: {str(e)}'}), 401
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401
    
    return decorated_function


def role_required(*roles):
    """
    Decorator to require specific user role(s)
    Usage: @role_required('admin', 'moderator')
    """
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            user_role = getattr(request, 'user_role', None)
            
            if not user_role or user_role not in roles:
                return jsonify({
                    'error': f'Requires one of: {", ".join(roles)}',
                    'your_role': user_role
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

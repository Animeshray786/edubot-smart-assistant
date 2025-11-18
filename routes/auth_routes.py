"""
Authentication Routes
JWT-based authentication endpoints
"""

from flask import Blueprint, request, jsonify, session
from backend.jwt_auth import JWTAuth, jwt_required
from backend.xss_protection import XSSProtection
from backend.error_handlers import ValidationError, AuthenticationError
from database.db_manager import DatabaseManager
import bcrypt

auth_bp = Blueprint('auth', __name__)

# Initialize JWT auth (will be set by app)
jwt_auth = None

def init_auth(app):
    """Initialize authentication with app"""
    global jwt_auth
    jwt_auth = JWTAuth(app.config.get('JWT_SECRET_KEY'))
    app.jwt_auth = jwt_auth
    return jwt_auth


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request JSON:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        {
            "access_token": "string",
            "refresh_token": "string",
            "user": {...}
        }
    """
    data = request.get_json()
    
    if not data:
        raise ValidationError('Request body required')
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        raise ValidationError('Username and password required')
    
    # Sanitize username (prevent XSS)
    username = XSSProtection.escape_html(username)
    
    # Get user from database
    db = DatabaseManager()
    user = db.authenticate_user(username, password)
    
    if not user:
        raise AuthenticationError('Invalid username or password')
    
    if not user.get('is_active'):
        raise AuthenticationError('Account is disabled')
    
    # Generate tokens
    access_token = jwt_auth.generate_access_token(
        user['user_id'],
        user['username'],
        user['role']
    )
    
    refresh_token = jwt_auth.generate_refresh_token(user['user_id'])
    
    # Store session info
    session['user_id'] = user['user_id']
    session['username'] = user['username']
    session['role'] = user['role']
    
    return jsonify({
        'success': True,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token
    
    Request JSON:
        {
            "refresh_token": "string"
        }
    
    Returns:
        {
            "access_token": "string"
        }
    """
    data = request.get_json()
    
    if not data or not data.get('refresh_token'):
        raise ValidationError('Refresh token required')
    
    refresh_token = data['refresh_token']
    
    # Generate new access token
    access_token = jwt_auth.refresh_access_token(refresh_token)
    
    if not access_token:
        raise AuthenticationError('Invalid or expired refresh token')
    
    return jsonify({
        'success': True,
        'access_token': access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """
    Logout endpoint (revoke tokens)
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        {
            "success": true
        }
    """
    # Get token from header
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split()[-1] if auth_header else None
    
    if token:
        jwt_auth.revoke_token(token)
    
    # Clear session
    session.clear()
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    
    Request JSON:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        {
            "success": true,
            "user_id": int
        }
    """
    data = request.get_json()
    
    if not data:
        raise ValidationError('Request body required')
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    # Validate inputs
    if not username or not email or not password:
        raise ValidationError('Username, email, and password required')
    
    # Sanitize inputs
    username = XSSProtection.escape_html(username)
    email = XSSProtection.escape_html(email)
    
    # Validate email format
    from backend.security_manager import InputValidator
    validator = InputValidator()
    
    if not validator.is_valid_email(email):
        raise ValidationError('Invalid email format', field='email')
    
    # Validate password strength
    if not validator.is_strong_password(password):
        raise ValidationError(
            'Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters',
            field='password'
        )
    
    # Create user
    db = DatabaseManager()
    
    try:
        user_id = db.create_user(username, email, password, role='user')
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        error_msg = str(e)
        if 'UNIQUE constraint' in error_msg or 'duplicate' in error_msg.lower():
            raise ValidationError('Username or email already exists')
        raise


@auth_bp.route('/me', methods=['GET'])
@jwt_required
def get_current_user():
    """
    Get current authenticated user info
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        {
            "user": {...}
        }
    """
    user_id = request.user_id
    
    db = DatabaseManager()
    user = db.get_user_by_id(user_id)
    
    if not user:
        raise AuthenticationError('User not found')
    
    return jsonify({
        'user': {
            'user_id': user['user_id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role'],
            'is_active': user['is_active'],
            'created_at': str(user['created_at'])
        }
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required
def change_password():
    """
    Change user password
    
    Headers:
        Authorization: Bearer <token>
    
    Request JSON:
        {
            "current_password": "string",
            "new_password": "string"
        }
    
    Returns:
        {
            "success": true
        }
    """
    data = request.get_json()
    
    if not data:
        raise ValidationError('Request body required')
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    
    if not current_password or not new_password:
        raise ValidationError('Current and new password required')
    
    # Validate new password strength
    from backend.security_manager import InputValidator
    validator = InputValidator()
    
    if not validator.is_strong_password(new_password):
        raise ValidationError(
            'Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters',
            field='new_password'
        )
    
    # Verify current password
    db = DatabaseManager()
    user = db.get_user_by_id(request.user_id)
    
    if not user:
        raise AuthenticationError('User not found')
    
    if not bcrypt.checkpw(current_password.encode('utf-8'), 
                         user['password_hash'].encode('utf-8')):
        raise ValidationError('Current password is incorrect', field='current_password')
    
    # Update password
    password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    # Update in database
    from sqlalchemy import update
    from database.models import User
    
    with db.get_session() as session:
        stmt = update(User).where(
            User.user_id == request.user_id
        ).values(
            password_hash=password_hash.decode('utf-8')
        )
        session.execute(stmt)
        session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Password changed successfully'
    }), 200


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Verify JWT token validity
    
    Request JSON:
        {
            "token": "string"
        }
    
    Returns:
        {
            "valid": bool,
            "payload": {...}
        }
    """
    data = request.get_json()
    
    if not data or not data.get('token'):
        raise ValidationError('Token required')
    
    token = data['token']
    
    try:
        payload = jwt_auth.verify_token(token)
        return jsonify({
            'valid': True,
            'payload': {
                'user_id': payload['user_id'],
                'username': payload['username'],
                'role': payload['role'],
                'exp': payload['exp']
            }
        }), 200
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': str(e)
        }), 200

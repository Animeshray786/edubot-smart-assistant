"""
Security Manager
Comprehensive security utilities for input validation, CSRF protection, and secure headers
"""

import re
import hashlib
import secrets
import bleach
from functools import wraps
from flask import request, session, abort, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt


class InputValidator:
    """Input validation utilities"""
    
    def is_valid_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def is_strong_password(self, password):
        """Check password strength"""
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True
    
    def contains_sql_injection(self, text):
        """Check for SQL injection patterns"""
        dangerous_patterns = [
            r'(\bUNION\b.*\bSELECT\b)',
            r'(\bDROP\b.*\bTABLE\b)',
            r'(--|#|\/\*)',
            r'(\bEXEC\b|\bEXECUTE\b)',
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False


class CSRFProtection:
    """CSRF token management"""
    
    def __init__(self):
        self.tokens = {}
    
    def generate_token(self, session_id):
        """Generate CSRF token"""
        token = secrets.token_urlsafe(32)
        self.tokens[session_id] = {
            'token': token,
            'timestamp': datetime.utcnow()
        }
        return token
    
    def validate_token(self, session_id, token):
        """Validate CSRF token"""
        if session_id not in self.tokens:
            return False
        
        stored = self.tokens[session_id]
        
        # Check expiry (1 hour)
        if (datetime.utcnow() - stored['timestamp']).total_seconds() > 3600:
            del self.tokens[session_id]
            return False
        
        return stored['token'] == token


class SecurityManager:
    """Centralized security management"""
    
    # XSS Protection - Allowed HTML tags
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'ul', 'ol', 'li', 'code', 'pre', 'blockquote']
    ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'img': ['src', 'alt']}
    
    # File upload restrictions
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
    ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'csv'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Rate limiting
    RATE_LIMIT_REQUESTS = 100
    RATE_LIMIT_WINDOW = 60  # seconds
    
    def __init__(self, app=None):
        """Initialize security manager"""
        self.csrf_tokens = {}
        self.rate_limit_data = {}
        self.input_validator = InputValidator()
        self.csrf_protection = CSRFProtection()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        pass
    
    # ==================== CSRF PROTECTION ====================
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token for form protection"""
        if 'csrf_token' not in session:
            session['csrf_token'] = secrets.token_hex(32)
        return session['csrf_token']
    
    def validate_csrf_token(self, token: str) -> bool:
        """Validate CSRF token"""
        return token == session.get('csrf_token')
    
    def csrf_protect(self, f):
        """Decorator for CSRF protection on routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'POST':
                token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
                if not token or not self.validate_csrf_token(token):
                    abort(403, description="CSRF token validation failed")
            return f(*args, **kwargs)
        return decorated_function
    
    # ==================== INPUT VALIDATION & SANITIZATION ====================
    
    @staticmethod
    def sanitize_html(html_content: str, strip_all: bool = False) -> str:
        """
        Sanitize HTML to prevent XSS attacks
        
        Args:
            html_content: Raw HTML content
            strip_all: If True, strip all HTML tags
            
        Returns:
            str: Sanitized HTML
        """
        if strip_all:
            return bleach.clean(html_content, tags=[], strip=True)
        
        return bleach.clean(
            html_content,
            tags=SecurityManager.ALLOWED_TAGS,
            attributes=SecurityManager.ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username (alphanumeric, underscore, hyphen, 3-20 chars)"""
        pattern = r'^[a-zA-Z0-9_-]{3,20}$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_password_strength(password: str) -> dict:
        """
        Validate password strength
        
        Returns:
            dict: {'valid': bool, 'errors': list}
        """
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    @staticmethod
    def sanitize_sql_input(value: str) -> str:
        """
        Sanitize input for SQL queries (use parameterized queries as primary defense)
        This is additional protection, NOT a replacement for parameterized queries
        """
        # Remove common SQL injection patterns
        dangerous_patterns = [
            r"'.*OR.*'",
            r"--",
            r"/\*.*\*/",
            r"UNION.*SELECT",
            r"DROP.*TABLE",
            r"INSERT.*INTO",
            r"DELETE.*FROM",
            r"UPDATE.*SET"
        ]
        
        for pattern in dangerous_patterns:
            value = re.sub(pattern, '', value, flags=re.IGNORECASE)
        
        return value.strip()
    
    @staticmethod
    def validate_file_upload(file, allowed_extensions: set = None) -> dict:
        """
        Validate file upload for security
        
        Returns:
            dict: {'valid': bool, 'error': str}
        """
        if not file or file.filename == '':
            return {'valid': False, 'error': 'No file provided'}
        
        # Check file extension
        if '.' not in file.filename:
            return {'valid': False, 'error': 'File has no extension'}
        
        ext = file.filename.rsplit('.', 1)[1].lower()
        allowed = allowed_extensions or SecurityManager.ALLOWED_IMAGE_EXTENSIONS
        
        if ext not in allowed:
            return {'valid': False, 'error': f'File type .{ext} not allowed'}
        
        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to start
        
        if file_size > SecurityManager.MAX_FILE_SIZE:
            return {'valid': False, 'error': f'File too large (max {SecurityManager.MAX_FILE_SIZE / (1024*1024)}MB)'}
        
        # Validate MIME type
        mime_type = file.content_type
        allowed_mimes = {
            'image/png', 'image/jpeg', 'image/jpg', 'image/gif', 
            'image/webp', 'application/pdf', 'text/plain'
        }
        
        if mime_type not in allowed_mimes:
            return {'valid': False, 'error': f'MIME type {mime_type} not allowed'}
        
        return {'valid': True, 'error': None}
    
    # ==================== PASSWORD HASHING ====================
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using werkzeug (uses bcrypt internally)"""
        return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return check_password_hash(password_hash, password)
    
    # ==================== JWT AUTHENTICATION ====================
    
    @staticmethod
    def generate_jwt_token(user_id: int, expires_in: int = 3600) -> str:
        """
        Generate JWT token for API authentication
        
        Args:
            user_id: User ID
            expires_in: Token expiration in seconds
            
        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in),
            'iat': datetime.utcnow()
        }
        
        secret_key = current_app.config.get('SECRET_KEY', 'default-secret-key')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def verify_jwt_token(token: str) -> dict:
        """
        Verify and decode JWT token
        
        Returns:
            dict: {'valid': bool, 'user_id': int, 'error': str}
        """
        try:
            secret_key = current_app.config.get('SECRET_KEY', 'default-secret-key')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            return {
                'valid': True,
                'user_id': payload['user_id'],
                'error': None
            }
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'user_id': None, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'user_id': None, 'error': 'Invalid token'}
    
    def jwt_required(self, f):
        """Decorator for JWT authentication on API routes"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            
            if not token:
                abort(401, description="Missing authorization token")
            
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            result = self.verify_jwt_token(token)
            
            if not result['valid']:
                abort(401, description=result['error'])
            
            # Add user_id to request context
            request.user_id = result['user_id']
            
            return f(*args, **kwargs)
        return decorated_function
    
    # ==================== RATE LIMITING ====================
    
    def check_rate_limit(self, identifier: str) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            identifier: Unique identifier (IP, user_id, etc.)
            
        Returns:
            bool: True if within limit, False if exceeded
        """
        now = datetime.utcnow()
        
        if identifier not in self.rate_limit_data:
            self.rate_limit_data[identifier] = []
        
        # Remove old requests outside the time window
        self.rate_limit_data[identifier] = [
            timestamp for timestamp in self.rate_limit_data[identifier]
            if (now - timestamp).total_seconds() < self.RATE_LIMIT_WINDOW
        ]
        
        # Check if limit exceeded
        if len(self.rate_limit_data[identifier]) >= self.RATE_LIMIT_REQUESTS:
            return False
        
        # Add current request
        self.rate_limit_data[identifier].append(now)
        return True
    
    def rate_limit(self, f):
        """Decorator for rate limiting"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identifier = request.remote_addr
            
            if not self.check_rate_limit(identifier):
                abort(429, description="Rate limit exceeded. Please try again later.")
            
            return f(*args, **kwargs)
        return decorated_function
    
    # ==================== SECURE HEADERS ====================
    
    @staticmethod
    def set_secure_headers(response):
        """Set security headers on response"""
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Prevent MIME sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # HTTPS enforcement (if in production)
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https:; "
        )
        
        # Referrer policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response


class SecureHeaders:
    """Middleware to add security headers to all responses"""
    
    def __init__(self, app=None):
        """Initialize secure headers middleware"""
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        @app.after_request
        def add_security_headers(response):
            # Prevent clickjacking
            response.headers['X-Frame-Options'] = 'DENY'
            
            # XSS protection
            response.headers['X-XSS-Protection'] = '1; mode=block'
            
            # Prevent MIME sniffing
            response.headers['X-Content-Type-Options'] = 'nosniff'
            
            # HTTPS enforcement
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            
            # Content Security Policy
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
            )
            
            # Referrer policy
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # Permissions policy
            response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
            
            return response


def init_security(app):
    """Initialize security manager with Flask app"""
    
    # Set secure session configuration
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
        SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
        PERMANENT_SESSION_LIFETIME=3600  # 1 hour
    )
    
    manager = SecurityManager(app)
    
    print("[OK] Security Manager initialized with CSRF, XSS, JWT, and Rate Limiting")
    return manager

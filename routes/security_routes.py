"""
Security Routes and CSRF Token Management
Endpoints for security features
"""

from flask import Blueprint, jsonify, session, request, current_app
from functools import wraps

security_bp = Blueprint('security', __name__)


def require_csrf(f):
    """Decorator to require CSRF token validation"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
            
            if not token:
                return jsonify({'error': 'CSRF token missing'}), 403
            
            session_id = session.get('session_id', request.remote_addr)
            
            if not security_manager.csrf_protection.validate_token(session_id, token):
                return jsonify({'error': 'Invalid CSRF token'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


@security_bp.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    """
    Get CSRF token for the current session
    
    Returns:
        JSON with CSRF token
    """
    try:
        security_manager = getattr(current_app, 'security_manager', None)
        if not security_manager:
            return jsonify({'error': 'Security manager not available'}), 500
        
        # Get or create session ID
        if 'session_id' not in session:
            import secrets
            session['session_id'] = secrets.token_urlsafe(16)
        
        session_id = session['session_id']
        
        # Generate CSRF token
        token = security_manager.csrf_protection.generate_token(session_id)
        
        return jsonify({
            'csrf_token': token,
            'expires_in': 3600  # 1 hour
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/validate-input', methods=['POST'])
def validate_input():
    """
    Validate user input for security issues
    
    Request Body:
        {
            "text": "Input text to validate",
            "type": "email|url|username|password|phone"
        }
    
    Returns:
        JSON with validation result
    """
    try:
        security_manager = getattr(current_app, 'security_manager', None)
        if not security_manager:
            return jsonify({'error': 'Security manager not available'}), 500
        
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        input_type = data.get('type', 'text')
        
        result = {
            'is_valid': True,
            'sanitized': text,
            'errors': []
        }
        
        # Type-specific validation
        if input_type == 'email':
            if not security_manager.input_validator.is_valid_email(text):
                result['is_valid'] = False
                result['errors'].append('Invalid email format')
        
        elif input_type == 'url':
            if not security_manager.input_validator.is_valid_url(text):
                result['is_valid'] = False
                result['errors'].append('Invalid URL format')
        
        elif input_type == 'username':
            if not security_manager.input_validator.is_valid_username(text):
                result['is_valid'] = False
                result['errors'].append('Username must be 3-20 alphanumeric characters')
        
        elif input_type == 'password':
            if not security_manager.input_validator.is_strong_password(text):
                result['is_valid'] = False
                result['errors'].append('Password must be at least 8 characters with uppercase, lowercase, numbers, and special characters')
        
        elif input_type == 'phone':
            if not security_manager.input_validator.is_valid_phone(text):
                result['is_valid'] = False
                result['errors'].append('Invalid phone number format')
        
        # Check for XSS
        sanitized = security_manager.sanitize_input(text)
        if sanitized != text:
            result['sanitized'] = sanitized
            result['warnings'] = ['Input contains potentially dangerous content and was sanitized']
        
        # Check for SQL injection
        if security_manager.input_validator.contains_sql_injection(text):
            result['is_valid'] = False
            result['errors'].append('Input contains potential SQL injection patterns')
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/sanitize-html', methods=['POST'])
def sanitize_html():
    """
    Sanitize HTML content
    
    Request Body:
        {
            "html": "HTML content to sanitize",
            "allowed_tags": ["p", "b", "i", "u", "a"]  # Optional
        }
    
    Returns:
        JSON with sanitized HTML
    """
    try:
        security_manager = getattr(current_app, 'security_manager', None)
        if not security_manager:
            return jsonify({'error': 'Security manager not available'}), 500
        
        data = request.get_json()
        
        if not data or 'html' not in data:
            return jsonify({'error': 'HTML content is required'}), 400
        
        html = data['html']
        allowed_tags = data.get('allowed_tags')
        
        # Sanitize HTML
        if allowed_tags and hasattr(security_manager.input_validator, 'sanitize_html'):
            sanitized = security_manager.input_validator.sanitize_html(html, allowed_tags)
        else:
            sanitized = security_manager.prevent_xss(html)
        
        return jsonify({
            'original': html,
            'sanitized': sanitized,
            'changed': html != sanitized
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/check-password-strength', methods=['POST'])
def check_password_strength():
    """
    Check password strength
    
    Request Body:
        {
            "password": "password to check"
        }
    
    Returns:
        JSON with password strength analysis
    """
    try:
        data = request.get_json()
        
        if not data or 'password' not in data:
            return jsonify({'error': 'Password is required'}), 400
        
        password = data['password']
        
        # Analyze password
        result = {
            'strength': 'weak',
            'score': 0,
            'feedback': [],
            'is_strong': False
        }
        
        # Length check
        if len(password) < 8:
            result['feedback'].append('Password should be at least 8 characters')
        else:
            result['score'] += 25
        
        # Uppercase check
        if any(c.isupper() for c in password):
            result['score'] += 25
        else:
            result['feedback'].append('Add uppercase letters')
        
        # Lowercase check
        if any(c.islower() for c in password):
            result['score'] += 25
        else:
            result['feedback'].append('Add lowercase letters')
        
        # Number check
        if any(c.isdigit() for c in password):
            result['score'] += 12
        else:
            result['feedback'].append('Add numbers')
        
        # Special character check
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            result['score'] += 13
        else:
            result['feedback'].append('Add special characters')
        
        # Determine strength
        if result['score'] >= 80:
            result['strength'] = 'strong'
            result['is_strong'] = True
        elif result['score'] >= 60:
            result['strength'] = 'medium'
        else:
            result['strength'] = 'weak'
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/rate-limit-status', methods=['GET'])
def rate_limit_status():
    """
    Get rate limit status for current user/IP
    
    Returns:
        JSON with rate limit information
    """
    try:
        user_id = session.get('user_id')
        client_ip = request.remote_addr
        identifier = f"user_{user_id}" if user_id else client_ip
        
        # Get rate limit info (would need to implement in rate_limiter)
        status = {
            'identifier': identifier,
            'type': 'user' if user_id else 'ip',
            'limits': {
                'requests_per_minute': 60,
                'requests_per_hour': 1000
            },
            'current_usage': {
                'requests_this_minute': 0,
                'requests_this_hour': 0
            },
            'reset_times': {
                'minute_resets_in': 60,
                'hour_resets_in': 3600
            }
        }
        
        return jsonify(status), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/security-headers', methods=['GET'])
def get_security_headers():
    """
    Get information about security headers
    
    Returns:
        JSON with security headers information
    """
    headers_info = {
        'Content-Security-Policy': {
            'enabled': True,
            'policy': "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net fonts.googleapis.com; font-src 'self' cdn.jsdelivr.net fonts.gstatic.com; img-src 'self' data: https:;"
        },
        'X-Frame-Options': {
            'enabled': True,
            'value': 'DENY'
        },
        'X-Content-Type-Options': {
            'enabled': True,
            'value': 'nosniff'
        },
        'Strict-Transport-Security': {
            'enabled': True,
            'value': 'max-age=31536000; includeSubDomains'
        },
        'X-XSS-Protection': {
            'enabled': True,
            'value': '1; mode=block'
        },
        'Referrer-Policy': {
            'enabled': True,
            'value': 'strict-origin-when-cross-origin'
        },
        'Permissions-Policy': {
            'enabled': True,
            'value': 'geolocation=(), microphone=(), camera=()'
        }
    }
    
    return jsonify(headers_info), 200

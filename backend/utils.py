"""
Utility functions for Hybrid Voice Chatbot
"""
import os
import uuid
import hashlib
import re
from datetime import datetime
from functools import wraps
from flask import session, jsonify


def generate_session_id():
    """Generate unique session ID"""
    return str(uuid.uuid4())


def generate_hash(text):
    """Generate SHA256 hash of text"""
    return hashlib.sha256(text.encode()).hexdigest()


def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    # Remove any non-alphanumeric characters except dots and dashes
    filename = re.sub(r'[^\w\s.-]', '', filename)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    return filename


def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def format_timestamp(dt):
    """Format datetime to readable string"""
    if not dt:
        return ''
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def time_ago(dt):
    """Convert datetime to 'time ago' format"""
    if not dt:
        return ''
    
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours != 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days != 1 else ""} ago'
    else:
        return format_timestamp(dt)


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return error_response('Authentication required', 401)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return error_response('Authentication required', 401)
        
        from database.models import User
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            return error_response('Admin access required', 403)
        
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required', 'status': 401}), 401
        if session.get('role') != 'admin':
            return jsonify({'error': 'Admin access required', 'status': 403}), 403
        return f(*args, **kwargs)
    return decorated_function


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_username(username):
    """Validate username format"""
    # Username: 3-50 characters, alphanumeric and underscore only
    pattern = r'^[a-zA-Z0-9_]{3,50}$'
    return re.match(pattern, username) is not None


def validate_password(password):
    """Validate password strength"""
    # At least 6 characters
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    # Contains at least one letter and one number
    if not re.search(r'[a-zA-Z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Valid password"


def truncate_text(text, max_length=100, suffix='...'):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + suffix


def clean_text(text):
    """Clean and normalize text"""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text.strip()


def pagination_info(page, per_page, total_items):
    """Generate pagination information"""
    total_pages = (total_items + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return {
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages,
        'has_prev': has_prev,
        'has_next': has_next,
        'prev_page': page - 1 if has_prev else None,
        'next_page': page + 1 if has_next else None
    }


def success_response(data=None, message='Success', status=200):
    """Generate success response"""
    response = {
        'status': 'success',
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status


def error_response(message='Error', status=400, errors=None):
    """Generate error response"""
    response = {
        'status': 'error',
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status


def get_client_ip(request):
    """Get client IP address from request"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        ip = request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        ip = request.environ.get('REMOTE_ADDR', 'Unknown')
    return ip


def get_user_agent(request):
    """Get user agent from request"""
    return request.environ.get('HTTP_USER_AGENT', 'Unknown')


class RateLimiter:
    """Simple rate limiter"""
    def __init__(self, max_requests=100, time_window=3600):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, identifier):
        """Check if request is allowed"""
        now = datetime.utcnow().timestamp()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < self.time_window
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Add new request
        self.requests[identifier].append(now)
        return True


def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

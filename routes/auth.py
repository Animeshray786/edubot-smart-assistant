"""
Authentication Routes for Hybrid Voice Chatbot
Handles user registration, login, and logout
"""
from flask import Blueprint, request, session, jsonify
from database.models import User
from database.db_manager import DatabaseManager
from database import db
from backend.utils import (
    validate_email, validate_username, validate_password,
    success_response, error_response, get_client_ip, generate_session_id
)

auth_bp = Blueprint('auth', __name__)
db_manager = DatabaseManager(db)


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return error_response('All fields are required', 400)
        
        # Validate username
        if not validate_username(username):
            return error_response('Invalid username. Use 3-50 alphanumeric characters or underscore', 400)
        
        # Validate email
        if not validate_email(email):
            return error_response('Invalid email format', 400)
        
        # Validate password
        valid, msg = validate_password(password)
        if not valid:
            return error_response(msg, 400)
        
        # Check if user already exists
        if db_manager.get_user_by_username(username):
            return error_response('Username already exists', 400)
        
        if db_manager.get_user_by_email(email):
            return error_response('Email already registered', 400)
        
        # Create user
        user = db_manager.create_user(username, email, password, role='user')
        
        # Auto-login after registration
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['role'] = user.role
        session['session_id'] = generate_session_id()
        
        # Create session record
        db_manager.create_session(
            session_id=session['session_id'],
            user_id=user.user_id,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent')
        )
        
        return success_response({
            'user': user.to_dict(),
            'message': 'Registration successful'
        }, 'Registration successful', 201)
        
    except Exception as e:
        print(f"Error in registration: {str(e)}")
        return error_response('Registration failed', 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login a user"""
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return error_response('Username and password required', 400)
        
        # Get user
        user = db_manager.get_user_by_username(username)
        if not user:
            user = db_manager.get_user_by_email(username)  # Allow login with email
        
        if not user or not user.check_password(password):
            return error_response('Invalid credentials', 401)
        
        if not user.is_active:
            return error_response('Account is disabled', 403)
        
        # Create session
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['role'] = user.role
        session['session_id'] = generate_session_id()
        
        # Create session record
        db_manager.create_session(
            session_id=session['session_id'],
            user_id=user.user_id,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent')
        )
        
        return success_response({
            'user': user.to_dict(),
            'message': 'Login successful'
        }, 'Login successful')
        
    except Exception as e:
        print(f"Error in login: {str(e)}")
        return error_response('Login failed', 500)


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout a user"""
    try:
        # End session in database
        if 'session_id' in session:
            db_manager.end_session(session['session_id'])
        
        # Clear session
        session.clear()
        
        return success_response(message='Logout successful')
        
    except Exception as e:
        print(f"Error in logout: {str(e)}")
        return error_response('Logout failed', 500)


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    try:
        if 'user_id' not in session:
            return error_response('Not authenticated', 401)
        
        user = db_manager.get_user_by_id(session['user_id'])
        if not user:
            session.clear()
            return error_response('User not found', 404)
        
        return success_response(user.to_dict())
        
    except Exception as e:
        print(f"Error getting current user: {str(e)}")
        return error_response('Failed to get user', 500)


@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if session is valid"""
    try:
        if 'user_id' in session:
            return success_response({
                'authenticated': True,
                'user_id': session['user_id'],
                'username': session.get('username'),
                'role': session.get('role')
            })
        else:
            return success_response({'authenticated': False})
            
    except Exception as e:
        print(f"Error checking session: {str(e)}")
        return error_response('Failed to check session', 500)

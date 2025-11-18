"""
Hybrid Voice-Enabled AI Chatbot with Self-Learning Mode and Feedback System
Main Flask Application

Project: Final Year Engineering
Author: AI Project Team
Date: November 2025
Version: 1.0.0
"""

from flask import Flask, render_template, session, jsonify, request
from flask_cors import CORS
from flask_session import Session
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Production configuration class
class ProductionConfig:
    """Production environment configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'edubot-production-secret-key-change-this')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///chatbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    
    # Session configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload configuration
    UPLOAD_FOLDER = 'uploads'
    AIML_DIR = 'aiml'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # CORS
    CORS_ORIGINS = ['*']  # Update with your domain in production
    
    # Admin defaults
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@edubot.com')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')

# Initialize Flask app
app = Flask(__name__, 
            template_folder='frontend',
            static_folder='static')

# Load configuration based on environment
try:
    if os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER'):
        app.config.from_object(ProductionConfig)
        print("[OK] Running in PRODUCTION mode")
    else:
        from config import get_config
        config_obj = get_config()
        app.config.from_object(config_obj)
        print("[OK] Running in DEVELOPMENT mode")
except Exception as e:
    print(f"[WARNING] Config error: {e}, using production config")
    app.config.from_object(ProductionConfig)

# Initialize extensions
from database import db
db.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/*": {"origins": app.config['CORS_ORIGINS']}})

# Session configuration
Session(app)

# Create required directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AIML_DIR'], exist_ok=True)
os.makedirs('static/uploads', exist_ok=True)

# Import blueprints
from routes.api import api_bp
from routes.admin import admin_bp
from routes.chat import chat_bp
from routes.auth import auth_bp
from routes.lecture_routes import lecture_bp
from routes.admin_lecture import admin_lecture_bp

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(chat_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(lecture_bp, url_prefix='/api/lecture')
app.register_blueprint(admin_lecture_bp, url_prefix='/admin/lecture')

# Initialize AIML Engine
try:
    from backend.aiml_engine import AIMLEngine
    aiml_engine = AIMLEngine(app.config['AIML_DIR'])
    app.aiml_engine = aiml_engine
    print("[OK] AIML Engine initialized")
except Exception as e:
    print(f"[WARNING] AIML Engine failed: {e}")
    app.aiml_engine = None

# Initialize Database Manager
try:
    from database.db_manager import DatabaseManager
    db_manager = DatabaseManager(db)
    app.db_manager = db_manager
    print("[OK] Database Manager initialized")
except Exception as e:
    print(f"[WARNING] Database Manager failed: {e}")
    app.db_manager = None


def initialize_database():
    """Initialize database and create default admin"""
    with app.app_context():
        # Import models to ensure they're registered
        from database.lecture_notes_model import LectureNote, StudyQuestion, KeyConcept
        
        # Create database tables
        db.create_all()
        print("[OK] Database tables created")
        print("[OK] Database initialized")
        
        # Create default admin user if doesn't exist
        admin = db_manager.get_user_by_username(app.config['ADMIN_USERNAME'])
        if not admin:
            admin = db_manager.create_user(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                password=app.config['ADMIN_PASSWORD'],
                role='admin'
            )
            print(f"[OK] Admin user created: {admin.username}")


@app.before_request
def before_request():
    """Before each request"""
    session.permanent = True


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    if '/api/' in request.path:
        return jsonify({
            'error': 'Resource not found',
            'status': 404
        }), 404
    # Return simple message for non-API routes
    return jsonify({'error': 'Page not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return jsonify({
        'error': 'Internal server error',
        'status': 500
    }), 500


# Health check endpoint for cloud platforms
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': os.environ.get('FLASK_ENV', 'development')
    }), 200


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    if '/api/' in str(error):
        return jsonify({
            'error': 'Internal server error',
            'status': 500
        }), 500
    return render_template('500.html'), 500


@app.errorhandler(403)
def forbidden(error):
    """403 error handler"""
    return jsonify({
        'error': 'Forbidden',
        'status': 403
    }), 403


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'aiml_patterns': aiml_engine.get_pattern_count()
    }), 200


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.context_processor
def inject_globals():
    """Inject global variables into templates"""
    return {
        'app_name': 'Hybrid Voice Chatbot',
        'version': '1.0.0',
        'year': datetime.now().year
    }


if __name__ == '__main__':
    # Create database tables and initialize
    with app.app_context():
        db.create_all()
        print("\n" + "="*50)
        print("[OK] Database initialized")
        
        # Create default admin user if doesn't exist
        admin = db_manager.get_user_by_username(app.config['ADMIN_USERNAME'])
        if not admin:
            admin = db_manager.create_user(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                password=app.config['ADMIN_PASSWORD'],
                role='admin'
            )
            print(f"[OK] Admin user created: {admin.username}")
        
        print(f"[OK] AIML Engine loaded ({aiml_engine.get_pattern_count()} patterns)")
        print(f"[OK] Flask app ready on http://localhost:5000")
        print("="*50 + "\n")
    
    # Get local IP for network access
    import socket
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"""
╔═══════════════════════════════════════════════════════╗
║          EduBot - Smart Student Assistant             ║
╠═══════════════════════════════════════════════════════╣
║  Local Access:    http://localhost:5000               ║
║  Network Access:  http://{local_ip}:5000              ║
╠═══════════════════════════════════════════════════════╣
║  Share the Network URL with anyone on the same WiFi   ║
║  to test your chatbot!                                ║
╚═══════════════════════════════════════════════════════╝
        """)
    except:
        pass
    
    # Run Flask development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config['DEBUG']
    )

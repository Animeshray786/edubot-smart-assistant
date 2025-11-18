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
import sys

# Load environment variables
load_dotenv()

# Validate configuration
from backend.config_validator import ConfigValidator
is_valid, errors, warnings = ConfigValidator.validate_environment()

if errors:
    print("\n[ERROR] Configuration errors found:")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

if warnings:
    print("\n[WARNING] Configuration warnings:")
    for warning in warnings:
        print(f"  - {warning}")

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

# Initialize logging system
from backend.logging_system import StructuredLogger
logger = StructuredLogger.get_logger(
    name='edubot',
    log_file=os.getenv('LOG_FILE', 'logs/edubot.log'),
    level=os.getenv('LOG_LEVEL', 'INFO'),
    max_bytes=int(os.getenv('LOG_MAX_SIZE', 10485760)),
    backup_count=int(os.getenv('LOG_BACKUP_COUNT', 5))
)
app.logger = logger
logger.info('EduBot application starting...')

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
from routes.admin_advanced import admin_advanced_bp
from routes.i18n_routes import i18n_bp
from routes.context_routes import context_bp
from routes.autocomplete_routes import autocomplete_bp
from routes.image_routes import image_bp
from routes.security_routes import security_bp

# Register error handlers
from backend.error_handlers import register_error_handlers
register_error_handlers(app)
logger.info('Error handlers registered')

# Register blueprints
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(chat_bp, url_prefix='/')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(lecture_bp, url_prefix='/api/lecture')
app.register_blueprint(admin_lecture_bp, url_prefix='/admin/lecture')
app.register_blueprint(admin_advanced_bp, url_prefix='/admin/advanced')
app.register_blueprint(i18n_bp, url_prefix='/api/i18n')
app.register_blueprint(context_bp, url_prefix='/api/context')
app.register_blueprint(autocomplete_bp, url_prefix='/api/autocomplete')
app.register_blueprint(image_bp, url_prefix='/api/image')
app.register_blueprint(security_bp, url_prefix='/api/security')

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

# Initialize I18n Support
try:
    from backend.i18n_manager import init_i18n
    i18n = init_i18n(app)
    app.i18n = i18n
    print("[OK] I18n Manager initialized")
except Exception as e:
    print(f"[WARNING] I18n initialization failed: {e}")
    app.i18n = None

# Initialize Context Memory Manager
try:
    from backend.context_manager import init_context_manager
    context_mgr = init_context_manager(app)
    app.context_manager = context_mgr
except Exception as e:
    print(f"[WARNING] Context Manager initialization failed: {e}")
    app.context_manager = None

# Initialize Autocomplete Engine
try:
    from backend.autocomplete_engine import init_autocomplete
    autocomplete = init_autocomplete(app.aiml_engine)
    app.autocomplete = autocomplete
except Exception as e:
    print(f"[WARNING] Autocomplete Engine initialization failed: {e}")
    app.autocomplete = None

# Initialize Image Processor
try:
    from backend.image_processor import init_image_processor
    img_processor = init_image_processor()
    app.image_processor = img_processor
except Exception as e:
    print(f"[WARNING] Image Processor initialization failed: {e}")
    app.image_processor = None

# Initialize Security Manager
try:
    from backend.security_manager import SecurityManager, SecureHeaders
    security_manager = SecurityManager(app)
    secure_headers = SecureHeaders(app)
    app.security_manager = security_manager
    print("[OK] Security Manager initialized")
    print("[OK] Secure Headers middleware enabled")
except Exception as e:
    print(f"[WARNING] Security Manager initialization failed: {e}")
    app.security_manager = None

# Initialize JWT Authentication
try:
    from routes.auth_routes import init_auth
    jwt_auth = init_auth(app)
    app.jwt_auth = jwt_auth
    print("[OK] JWT Authentication initialized")
except Exception as e:
    print(f"[WARNING] JWT Auth initialization failed: {e}")
    app.jwt_auth = None

# Initialize XSS Protection
try:
    from backend.xss_protection import XSSProtection
    xss_protection = XSSProtection()
    app.xss_protection = xss_protection
    print("[OK] XSS Protection initialized")
except Exception as e:
    print(f"[WARNING] XSS Protection initialization failed: {e}")
    app.xss_protection = None

# Initialize Advanced Features
try:
    from backend.performance_monitor import performance_monitor
    from backend.rate_limiter import rate_limiter
    from backend.knowledge_gap_analyzer import KnowledgeGapAnalyzer
    
    app.performance_monitor = performance_monitor
    app.rate_limiter = rate_limiter
    app.knowledge_gap = KnowledgeGapAnalyzer(db)
    
    print("[OK] Performance Monitor initialized")
    print("[OK] Rate Limiter initialized")
    print("[OK] Knowledge Gap Analyzer initialized")
except Exception as e:
    print(f"[WARNING] Advanced features initialization failed: {e}")

# Initialize API Documentation
try:
    from backend.api_documentation import init_api_docs
    api_docs = init_api_docs(app)
    app.api_docs = api_docs
except Exception as e:
    print(f"[WARNING] API Documentation initialization failed: {e}")


# Request/Response Logging Middleware
import time
from backend.logging_system import StructuredLogger

@app.before_request
def log_request_start():
    """Log request start time"""
    request.start_time = time.time()

@app.after_request
def log_request_end(response):
    """Log request completion"""
    if hasattr(request, 'start_time'):
        duration_ms = (time.time() - request.start_time) * 1000
        user_id = getattr(request, 'user_id', None)
        
        StructuredLogger.log_request(
            app.logger,
            request,
            response.status_code,
            duration_ms,
            user_id
        )
    
    return response


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
    """Before each request - rate limiting and performance tracking"""
    import time
    from flask import request, jsonify
    
    # Set session permanent
    session.permanent = True
    
    # Track request start time
    request.start_time = time.time()
    
    # Get client identifier (IP or user_id)
    client_ip = request.remote_addr
    user_id = session.get('user_id')
    identifier = f"user_{user_id}" if user_id else client_ip
    
    # Check rate limit for API endpoints
    if request.path.startswith('/api/'):
        try:
            from backend.rate_limiter import rate_limiter
            
            limit_type = 'user' if user_id else 'ip'
            result = rate_limiter.check_rate_limit(identifier, limit_type)
            
            if not result['allowed']:
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'reason': result['reason'],
                    'retry_after': result.get('retry_after'),
                    'limit': result.get('limit'),
                    'period': result.get('period')
                })
                response.status_code = 429
                response.headers['Retry-After'] = str(result.get('retry_after', 60))
                return response
        except:
            pass  # If rate limiter fails, allow request


@app.after_request
def after_request(response):
    """After each request - track performance"""
    import time
    from flask import request
    
    # Calculate request duration
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        
        # Track in performance monitor
        try:
            from backend.performance_monitor import performance_monitor
            
            user_id = session.get('user_id')
            performance_monitor.track_request(
                endpoint=request.endpoint or request.path,
                method=request.method,
                duration=duration,
                status_code=response.status_code,
                user_id=user_id
            )
        except:
            pass  # If tracking fails, don't break request
    
    return response


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

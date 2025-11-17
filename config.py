"""
Configuration file for Hybrid Voice Chatbot
Manages different environment configurations
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask Configuration
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-please-change')
    
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///chatbot.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # MongoDB Configuration (Optional)
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/chatbot')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(
        seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 604800))
    )
    SESSION_COOKIE_SECURE = False  # Set True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Upload Configuration
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__), 
        os.getenv('UPLOAD_FOLDER', 'static/uploads')
    )
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'wav', 'mp3'}
    
    # AIML Configuration
    AIML_DIR = os.path.join(
        os.path.dirname(__file__),
        os.getenv('AIML_DIR', 'aiml')
    )
    
    # Voice Configuration
    VOICE_ENABLED = os.getenv('VOICE_ENABLED', 'True').lower() == 'true'
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'gtts')  # gtts or pyttsx3
    LANGUAGE = os.getenv('LANGUAGE', 'en')
    
    # API Configuration
    API_VERSION = os.getenv('API_VERSION', 'v1')
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100
    
    # Admin Configuration
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@chatbot.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')
    
    # Learning Module Configuration
    LEARNING_MODE_ENABLED = True
    AUTO_APPROVE_THRESHOLD = 0.95  # Confidence threshold for auto-approval
    MIN_FEEDBACK_FOR_LEARNING = 3
    
    # Analytics Configuration
    ANALYTICS_ENABLED = True
    ANALYTICS_RETENTION_DAYS = 90


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Use MySQL in production
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://chatbot_user:password@localhost/chatbot_prod'
    )
    SQLALCHEMY_ECHO = False
    
    # Security enhancements
    SECRET_KEY = os.getenv('SECRET_KEY', 'edubot-prod-key-' + os.urandom(24).hex())


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    LEARNING_MODE_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(config_name=None):
    """Get configuration object"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    return config.get(config_name, config['default'])

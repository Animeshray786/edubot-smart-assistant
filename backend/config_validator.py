"""
Configuration Validator
Validates environment variables and application configuration
"""

import os
import re
from typing import Dict, List, Tuple, Any
from pathlib import Path

class ConfigValidator:
    """Validates application configuration"""
    
    # Required environment variables
    REQUIRED_VARS = [
        'SECRET_KEY',
        'JWT_SECRET_KEY',
        'CSRF_SECRET_KEY'
    ]
    
    # Optional but recommended variables
    RECOMMENDED_VARS = [
        'DATABASE_URL',
        'REDIS_URL',
        'MAIL_SERVER',
        'LOG_LEVEL'
    ]
    
    # Security checks
    WEAK_SECRETS = [
        'change-this',
        'your-secret-key',
        'default',
        'test',
        '123456',
        'password'
    ]
    
    @staticmethod
    def validate_environment() -> Tuple[bool, List[str], List[str]]:
        """
        Validate environment configuration
        
        Returns:
            tuple: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        # Check required variables
        for var in ConfigValidator.REQUIRED_VARS:
            value = os.getenv(var)
            if not value:
                errors.append(f'Missing required environment variable: {var}')
            elif any(weak in value.lower() for weak in ConfigValidator.WEAK_SECRETS):
                warnings.append(f'{var} appears to use a weak/default value')
            elif len(value) < 32:
                warnings.append(f'{var} should be at least 32 characters for security')
        
        # Check recommended variables
        for var in ConfigValidator.RECOMMENDED_VARS:
            if not os.getenv(var):
                warnings.append(f'Recommended environment variable not set: {var}')
        
        # Validate specific configurations
        
        # Check database URL format
        db_url = os.getenv('DATABASE_URL', '')
        if db_url and not re.match(r'^(sqlite|postgresql|mysql):\/\/', db_url):
            warnings.append('DATABASE_URL format may be invalid')
        
        # Check email configuration
        if os.getenv('MAIL_SERVER'):
            if not os.getenv('MAIL_USERNAME'):
                warnings.append('MAIL_SERVER set but MAIL_USERNAME missing')
            if not os.getenv('MAIL_PASSWORD'):
                warnings.append('MAIL_SERVER set but MAIL_PASSWORD missing')
        
        # Check upload folder exists
        upload_folder = os.getenv('UPLOAD_FOLDER', 'uploads')
        if not os.path.exists(upload_folder):
            warnings.append(f'Upload folder does not exist: {upload_folder}')
        
        # Check log directory
        log_file = os.getenv('LOG_FILE', 'logs/edubot.log')
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            warnings.append(f'Log directory does not exist: {log_dir}')
        
        # Production checks
        if os.getenv('FLASK_ENV') == 'production':
            if os.getenv('FLASK_DEBUG', '').lower() == 'true':
                errors.append('DEBUG mode enabled in production!')
            
            if not os.getenv('SESSION_COOKIE_SECURE', '').lower() == 'true':
                warnings.append('SESSION_COOKIE_SECURE should be True in production')
            
            if not os.getenv('ENABLE_HSTS', '').lower() == 'true':
                warnings.append('HSTS should be enabled in production')
        
        is_valid = len(errors) == 0
        return is_valid, errors, warnings
    
    @staticmethod
    def get_config_summary() -> Dict[str, Any]:
        """
        Get configuration summary (safe to display)
        
        Returns:
            dict: Configuration summary with sensitive data masked
        """
        def mask_value(value: str) -> str:
            """Mask sensitive values"""
            if not value or len(value) < 8:
                return '****'
            return value[:4] + '****' + value[-4:]
        
        summary = {
            'environment': os.getenv('FLASK_ENV', 'development'),
            'debug': os.getenv('FLASK_DEBUG', 'False'),
            'database': os.getenv('DATABASE_URL', 'Not set')[:20] + '...' if os.getenv('DATABASE_URL') else 'Not set',
            'redis_enabled': os.getenv('REDIS_ENABLED', 'False'),
            'mail_configured': bool(os.getenv('MAIL_SERVER')),
            'rate_limiting': os.getenv('RATE_LIMIT_ENABLED', 'True'),
            'logging_level': os.getenv('LOG_LEVEL', 'INFO'),
            'upload_folder': os.getenv('UPLOAD_FOLDER', 'uploads'),
            'features': {
                'voice': os.getenv('ENABLE_VOICE', 'True'),
                'image_processing': os.getenv('ENABLE_IMAGE_PROCESSING', 'True'),
                'lecture_notes': os.getenv('ENABLE_LECTURE_NOTES', 'True'),
                'analytics': os.getenv('ENABLE_ANALYTICS', 'True'),
                'i18n': os.getenv('ENABLE_I18N', 'True')
            },
            'security': {
                'secret_key_set': bool(os.getenv('SECRET_KEY')),
                'jwt_key_set': bool(os.getenv('JWT_SECRET_KEY')),
                'csrf_key_set': bool(os.getenv('CSRF_SECRET_KEY')),
                'hsts_enabled': os.getenv('ENABLE_HSTS', 'True'),
                'csp_enabled': os.getenv('ENABLE_CSP', 'True')
            }
        }
        
        return summary
    
    @staticmethod
    def create_env_file_if_missing():
        """Create .env file from .env.example if it doesn't exist"""
        env_path = Path('.env')
        example_path = Path('.env.example')
        
        if not env_path.exists() and example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print('[INFO] Created .env file from .env.example')
            print('[WARNING] Please update .env with your actual configuration!')
            return True
        
        return False

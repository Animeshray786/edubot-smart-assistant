"""
Comprehensive Security Tests
Tests for XSS protection, JWT auth, and security features
"""

import pytest
import json
from app import app
from database import db
from database.models import User

@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def test_user(client):
    """Create test user"""
    response = client.post('/auth/register', 
        json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Test123!@#'
        }
    )
    return response.get_json()

class TestXSSProtection:
    """Test XSS protection functionality"""
    
    def test_detect_script_tags(self):
        """Test detection of script tags"""
        from backend.xss_protection import XSSProtection
        
        malicious = '<script>alert("xss")</script>'
        is_safe, patterns = XSSProtection.detect_xss(malicious)
        
        assert not is_safe
        assert len(patterns) > 0
    
    def test_detect_event_handlers(self):
        """Test detection of event handlers"""
        from backend.xss_protection import XSSProtection
        
        malicious = '<img src=x onerror="alert(1)">'
        is_safe, patterns = XSSProtection.detect_xss(malicious)
        
        assert not is_safe
    
    def test_sanitize_html(self):
        """Test HTML sanitization"""
        from backend.xss_protection import XSSProtection
        
        dirty = '<p>Safe</p><script>alert("xss")</script>'
        clean = XSSProtection.sanitize_html(dirty)
        
        assert '<p>Safe</p>' in clean
        assert '<script>' not in clean
    
    def test_sanitize_url(self):
        """Test URL sanitization"""
        from backend.xss_protection import XSSProtection
        
        # Safe URLs
        assert XSSProtection.sanitize_url('https://example.com') == 'https://example.com'
        assert XSSProtection.sanitize_url('/relative/path') == '/relative/path'
        
        # Dangerous URLs
        assert XSSProtection.sanitize_url('javascript:alert(1)') == ''
        assert XSSProtection.sanitize_url('data:text/html,<script>') == ''


class TestJWTAuthentication:
    """Test JWT authentication functionality"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        response = client.post('/auth/register',
            json={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'Strong123!@#'
            }
        )
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'user_id' in data
    
    def test_register_weak_password(self, client):
        """Test registration with weak password"""
        response = client.post('/auth/register',
            json={
                'username': 'newuser',
                'email': 'new@example.com',
                'password': 'weak'
            }
        )
        
        assert response.status_code == 400
    
    def test_login_success(self, client, test_user):
        """Test successful login"""
        response = client.post('/auth/login',
            json={
                'username': 'testuser',
                'password': 'Test123!@#'
            }
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_invalid_credentials(self, client, test_user):
        """Test login with invalid credentials"""
        response = client.post('/auth/login',
            json={
                'username': 'testuser',
                'password': 'wrongpassword'
            }
        )
        
        assert response.status_code == 401
    
    def test_jwt_protected_route(self, client, test_user):
        """Test accessing protected route with JWT"""
        # Login first
        login_response = client.post('/auth/login',
            json={
                'username': 'testuser',
                'password': 'Test123!@#'
            }
        )
        
        token = login_response.get_json()['access_token']
        
        # Access protected route
        response = client.get('/auth/me',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['user']['username'] == 'testuser'
    
    def test_jwt_missing_token(self, client):
        """Test accessing protected route without token"""
        response = client.get('/auth/me')
        
        assert response.status_code == 401
    
    def test_jwt_invalid_token(self, client):
        """Test accessing protected route with invalid token"""
        response = client.get('/auth/me',
            headers={'Authorization': 'Bearer invalid-token'}
        )
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, test_user):
        """Test token refresh"""
        # Login first
        login_response = client.post('/auth/login',
            json={
                'username': 'testuser',
                'password': 'Test123!@#'
            }
        )
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # Refresh access token
        response = client.post('/auth/refresh',
            json={'refresh_token': refresh_token}
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_logout(self, client, test_user):
        """Test logout functionality"""
        # Login first
        login_response = client.post('/auth/login',
            json={
                'username': 'testuser',
                'password': 'Test123!@#'
            }
        )
        
        token = login_response.get_json()['access_token']
        
        # Logout
        response = client.post('/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200


class TestSQLInjectionPrevention:
    """Test SQL injection prevention"""
    
    def test_detect_union_based(self):
        """Test detection of UNION-based injection"""
        from backend.sql_injection_prevention import SQLInjectionPrevention
        
        sql_inj = SQLInjectionPrevention()
        malicious = "' UNION SELECT password FROM users--"
        
        is_safe, patterns = sql_inj.detect_sql_injection(malicious)
        assert not is_safe
    
    def test_detect_boolean_based(self):
        """Test detection of boolean-based injection"""
        from backend.sql_injection_prevention import SQLInjectionPrevention
        
        sql_inj = SQLInjectionPrevention()
        malicious = "1' OR '1'='1"
        
        is_safe, patterns = sql_inj.detect_sql_injection(malicious)
        assert not is_safe
    
    def test_detect_time_based(self):
        """Test detection of time-based injection"""
        from backend.sql_injection_prevention import SQLInjectionPrevention
        
        sql_inj = SQLInjectionPrevention()
        malicious = "'; WAITFOR DELAY '00:00:05'--"
        
        is_safe, patterns = sql_inj.detect_sql_injection(malicious)
        assert not is_safe
    
    def test_safe_input(self):
        """Test safe input passes validation"""
        from backend.sql_injection_prevention import SQLInjectionPrevention
        
        sql_inj = SQLInjectionPrevention()
        safe = "John's Bakery"
        
        is_safe, patterns = sql_inj.detect_sql_injection(safe)
        assert is_safe


class TestConfigValidator:
    """Test configuration validation"""
    
    def test_validate_environment(self):
        """Test environment validation"""
        from backend.config_validator import ConfigValidator
        
        is_valid, errors, warnings = ConfigValidator.validate_environment()
        
        # Should have some warnings in test environment
        assert isinstance(errors, list)
        assert isinstance(warnings, list)
    
    def test_get_config_summary(self):
        """Test configuration summary"""
        from backend.config_validator import ConfigValidator
        
        summary = ConfigValidator.get_config_summary()
        
        assert 'environment' in summary
        assert 'security' in summary
        assert 'features' in summary


class TestLoggingSystem:
    """Test logging system"""
    
    def test_get_logger(self):
        """Test logger creation"""
        from backend.logging_system import StructuredLogger
        
        logger = StructuredLogger.get_logger('test')
        assert logger is not None
        assert logger.name == 'test'
    
    def test_log_security_event(self):
        """Test security event logging"""
        from backend.logging_system import StructuredLogger
        
        logger = StructuredLogger.get_logger('test')
        
        # Should not raise exception
        StructuredLogger.log_security_event(
            logger,
            'test_event',
            'medium',
            {'detail': 'test'},
            user_id=1
        )


class TestErrorHandlers:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handler"""
        response = client.get('/api/nonexistent')
        
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_validation_error(self, client):
        """Test validation error"""
        response = client.post('/auth/register',
            json={}  # Missing required fields
        )
        
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

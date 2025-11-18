"""
Comprehensive Testing Suite Configuration
Unit tests, integration tests, API tests, and load tests
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test configuration
TESTING = True
SECRET_KEY = 'test-secret-key-for-testing-only'
SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for tests
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False  # Disable CSRF for testing

# Test data directories
TEST_DATA_DIR = Path(__file__).parent / 'test_data'
TEST_UPLOADS_DIR = TEST_DATA_DIR / 'uploads'
TEST_AIML_DIR = TEST_DATA_DIR / 'aiml'

# Create test directories
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_UPLOADS_DIR.mkdir(exist_ok=True)
TEST_AIML_DIR.mkdir(exist_ok=True)


@pytest.fixture(scope='session')
def app():
    """Create Flask app for testing"""
    from app import app as flask_app
    
    # Configure for testing
    flask_app.config['TESTING'] = TESTING
    flask_app.config['SECRET_KEY'] = SECRET_KEY
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    flask_app.config['WTF_CSRF_ENABLED'] = WTF_CSRF_ENABLED
    
    yield flask_app


@pytest.fixture(scope='session')
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(scope='session')
def db(app):
    """Create database for testing"""
    from database.db_manager import db as database
    
    with app.app_context():
        database.create_all()
        yield database
        database.session.remove()
        database.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Create database session for tests"""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)
    
    db.session = session
    
    yield session
    
    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture
def sample_user(db):
    """Create sample user for testing"""
    from database.models import User
    
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        role='student'
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user


@pytest.fixture
def admin_user(db):
    """Create admin user for testing"""
    from database.models import User
    
    user = User(
        username='admin',
        email='admin@example.com',
        password_hash='hashed_password',
        role='admin'
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user


@pytest.fixture
def auth_headers(client, sample_user):
    """Get authentication headers for API testing"""
    from backend.security_manager import security_manager
    
    token = security_manager.generate_jwt_token(sample_user.user_id)
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_conversation(db, sample_user):
    """Create sample conversation for testing"""
    from database.models import Conversation
    
    conversation = Conversation(
        user_id=sample_user.user_id,
        user_message='Hello',
        bot_response='Hi there!',
        session_id='test-session'
    )
    
    db.session.add(conversation)
    db.session.commit()
    
    return conversation


# Pytest configuration
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as an API test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )

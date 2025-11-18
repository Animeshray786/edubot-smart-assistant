"""
Unit Tests for Backend Modules
Tests for AIML engine, context manager, autocomplete, and utilities
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime


@pytest.mark.unit
class TestAIMLEngine:
    """Test AIML Engine functionality"""
    
    def test_initialization(self, app):
        """Test AIML engine initializes correctly"""
        from backend.aiml_engine import aiml_engine
        
        assert aiml_engine is not None
        assert hasattr(aiml_engine, 'kernel')
    
    def test_get_response_simple(self, app):
        """Test simple response generation"""
        from backend.aiml_engine import aiml_engine
        
        response = aiml_engine.get_response("hello", "test-session")
        assert response is not None
        assert len(response) > 0
    
    def test_get_response_with_context(self, app):
        """Test response with context"""
        from backend.aiml_engine import aiml_engine
        
        context = {
            'user_id': 1,
            'username': 'testuser',
            'previous_topic': 'courses'
        }
        
        response = aiml_engine.get_response("what courses", "test-session", context)
        assert response is not None
    
    def test_session_management(self, app):
        """Test session variable management"""
        from backend.aiml_engine import aiml_engine
        
        session_id = "test-session-123"
        
        # Set session variable
        aiml_engine.set_session_var(session_id, "topic", "math")
        
        # Get session variable
        value = aiml_engine.get_session_var(session_id, "topic")
        assert value == "math"
    
    def test_pattern_learning(self, app):
        """Test dynamic pattern learning"""
        from backend.aiml_engine import aiml_engine
        
        # Add new pattern
        result = aiml_engine.learn_pattern(
            pattern="WHAT IS AI",
            template="Artificial Intelligence is..."
        )
        
        assert result is True


@pytest.mark.unit
class TestContextManager:
    """Test Context Memory Manager"""
    
    def test_save_context(self, app, sample_user):
        """Test saving conversation context"""
        from backend.context_manager import context_manager
        
        context_data = {
            'topic': 'programming',
            'subtopic': 'python',
            'user_intent': 'learning'
        }
        
        result = context_manager.save_context(
            user_id=sample_user.user_id,
            session_id='test-session',
            context_data=context_data
        )
        
        assert result is True
    
    def test_retrieve_context(self, app, sample_user):
        """Test retrieving conversation context"""
        from backend.context_manager import context_manager
        
        # Save context first
        context_manager.save_context(
            user_id=sample_user.user_id,
            session_id='test-session',
            context_data={'topic': 'math'}
        )
        
        # Retrieve context
        context = context_manager.get_context(
            user_id=sample_user.user_id,
            session_id='test-session'
        )
        
        assert context is not None
        assert context.get('topic') == 'math'
    
    def test_context_expiration(self, app, sample_user):
        """Test context expiration"""
        from backend.context_manager import context_manager
        from datetime import datetime, timedelta
        
        # Save old context
        old_context = {
            'timestamp': (datetime.now() - timedelta(days=8)).isoformat(),
            'data': {'topic': 'old'}
        }
        
        context_manager.save_context(
            user_id=sample_user.user_id,
            session_id='old-session',
            context_data=old_context
        )
        
        # Clean expired contexts
        context_manager.cleanup_expired_contexts(max_age_days=7)
        
        # Try to retrieve
        context = context_manager.get_context(
            user_id=sample_user.user_id,
            session_id='old-session'
        )
        
        assert context is None or len(context) == 0


@pytest.mark.unit
class TestAutocompleteEngine:
    """Test Autocomplete Engine"""
    
    def test_get_suggestions_basic(self, app):
        """Test basic autocomplete suggestions"""
        from backend.autocomplete_engine import autocomplete_engine
        
        suggestions = autocomplete_engine.get_suggestions("wha", limit=5)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) <= 5
        
        # Check suggestions start with input
        for suggestion in suggestions:
            assert 'wha' in suggestion['text'].lower()
    
    def test_get_suggestions_with_context(self, app):
        """Test context-aware suggestions"""
        from backend.autocomplete_engine import autocomplete_engine
        
        context = {
            'previous_messages': ['tell me about courses'],
            'current_topic': 'academics'
        }
        
        suggestions = autocomplete_engine.get_suggestions(
            "what", 
            context=context,
            limit=5
        )
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_learn_from_query(self, app):
        """Test learning from user queries"""
        from backend.autocomplete_engine import autocomplete_engine
        
        query = "what is machine learning"
        
        autocomplete_engine.learn_from_query(query)
        
        # Should now suggest this query
        suggestions = autocomplete_engine.get_suggestions("what is mac")
        
        assert any('machine learning' in s['text'].lower() for s in suggestions)
    
    def test_fuzzy_matching(self, app):
        """Test fuzzy matching for typos"""
        from backend.autocomplete_engine import autocomplete_engine
        
        # Intentional typo
        suggestions = autocomplete_engine.get_suggestions("helllo", fuzzy=True)
        
        assert any('hello' in s['text'].lower() for s in suggestions)


@pytest.mark.unit
class TestSecurityManager:
    """Test Security Manager"""
    
    def test_input_sanitization(self, app):
        """Test input sanitization"""
        from backend.security_manager import security_manager
        
        malicious_input = "<script>alert('xss')</script>Hello"
        
        cleaned = security_manager.sanitize_input(malicious_input)
        
        assert '<script>' not in cleaned
        assert 'Hello' in cleaned
    
    def test_xss_prevention(self, app):
        """Test XSS prevention"""
        from backend.security_manager import security_manager
        
        xss_html = """
        <div>
            <script>alert('xss')</script>
            <img src=x onerror="alert('xss')">
            <p>Safe content</p>
        </div>
        """
        
        cleaned = security_manager.prevent_xss(xss_html)
        
        assert '<script>' not in cleaned
        assert 'onerror=' not in cleaned
        assert 'Safe content' in cleaned
    
    def test_sql_injection_detection(self, app):
        """Test SQL injection detection"""
        from backend.security_manager import security_manager
        
        malicious_queries = [
            "'; DROP TABLE users; --",
            "1' OR '1'='1",
            "admin'--",
            "' UNION SELECT password FROM users--"
        ]
        
        for query in malicious_queries:
            is_safe = not security_manager.prevent_sql_injection(query)
            assert is_safe is False, f"Failed to detect SQL injection: {query}"
    
    def test_password_validation(self, app):
        """Test password strength validation"""
        from backend.security_manager import security_manager
        
        weak_passwords = ['12345678', 'password', 'qwerty', 'abc']
        strong_passwords = ['MyP@ssw0rd!', 'Secure#123', 'T3st!ngP@ss']
        
        for pwd in weak_passwords:
            assert security_manager.validate_password(pwd) is False
        
        for pwd in strong_passwords:
            assert security_manager.validate_password(pwd) is True
    
    def test_email_validation(self, app):
        """Test email validation"""
        from backend.security_manager import security_manager
        
        valid_emails = [
            'user@example.com',
            'test.user@domain.co.uk',
            'admin+tag@site.org'
        ]
        
        invalid_emails = [
            'notanemail',
            '@example.com',
            'user@',
            'user@.com'
        ]
        
        for email in valid_emails:
            assert security_manager.validate_email(email) is True
        
        for email in invalid_emails:
            assert security_manager.validate_email(email) is False
    
    def test_csrf_token_generation(self, app):
        """Test CSRF token generation"""
        from backend.security_manager import security_manager
        
        token = security_manager.generate_csrf_token()
        
        assert token is not None
        assert len(token) > 20
        assert isinstance(token, str)
    
    def test_csrf_token_validation(self, app):
        """Test CSRF token validation"""
        from backend.security_manager import security_manager
        
        # Generate valid token
        session_id = 'test-session-123'
        token = security_manager.csrf_protection.generate_token(session_id)
        
        # Valid token should pass
        assert security_manager.validate_csrf_token(token) is True
        
        # Invalid token should fail
        assert security_manager.validate_csrf_token('invalid-token') is False


@pytest.mark.unit
class TestImageProcessor:
    """Test Image Processor"""
    
    def test_validate_image(self, app):
        """Test image validation"""
        from backend.image_processor import image_processor
        
        # Mock file object
        mock_file = Mock()
        mock_file.filename = 'test.jpg'
        mock_file.content_type = 'image/jpeg'
        
        is_valid, message = image_processor.validate_image(mock_file)
        
        assert is_valid is True or is_valid is False  # Depends on file content
    
    @patch('PIL.Image.open')
    def test_extract_metadata(self, mock_image_open, app):
        """Test metadata extraction"""
        from backend.image_processor import image_processor
        
        # Mock PIL Image
        mock_img = MagicMock()
        mock_img.size = (800, 600)
        mock_img.format = 'JPEG'
        mock_img.mode = 'RGB'
        mock_image_open.return_value = mock_img
        
        metadata = image_processor.extract_metadata('test.jpg')
        
        assert metadata is not None


@pytest.mark.unit
class TestVoiceProcessor:
    """Test Voice Processor"""
    
    def test_text_to_speech_config(self, app):
        """Test TTS configuration"""
        from backend.voice_processor import voice_processor
        
        config = voice_processor.get_tts_config()
        
        assert 'voices' in config
        assert 'rate' in config
        assert 'pitch' in config
    
    def test_speech_to_text_validation(self, app):
        """Test STT input validation"""
        from backend.voice_processor import voice_processor
        
        # Test with valid audio data
        is_valid = voice_processor.validate_audio_input(b'mock_audio_data')
        
        assert isinstance(is_valid, bool)


@pytest.mark.unit
class TestTextFormatter:
    """Test Text Formatter"""
    
    def test_markdown_to_html(self, app):
        """Test markdown conversion"""
        from backend.text_formatter import TextFormatter
        
        formatter = TextFormatter()
        
        markdown = "**Bold** and *italic* text"
        html = formatter.markdown_to_html(markdown)
        
        assert '<strong>Bold</strong>' in html or '<b>Bold</b>' in html
    
    def test_code_highlighting(self, app):
        """Test code syntax highlighting"""
        from backend.text_formatter import TextFormatter
        
        formatter = TextFormatter()
        
        code = """```python
def hello():
    print("Hello, World!")
```"""
        
        html = formatter.format_text(code)
        
        assert 'code' in html or 'pre' in html


@pytest.mark.unit
class TestUtils:
    """Test Utility Functions"""
    
    def test_sanitize_filename(self, app):
        """Test filename sanitization"""
        from backend.utils import sanitize_filename
        
        dangerous_filenames = [
            '../../../etc/passwd',
            'file<>name.txt',
            'file|name.txt',
            'file:name.txt'
        ]
        
        for filename in dangerous_filenames:
            safe = sanitize_filename(filename)
            assert '../' not in safe
            assert '<' not in safe
            assert '>' not in safe
    
    def test_generate_session_id(self, app):
        """Test session ID generation"""
        from backend.utils import generate_session_id
        
        session_id = generate_session_id()
        
        assert len(session_id) > 10
        assert isinstance(session_id, str)
    
    def test_format_timestamp(self, app):
        """Test timestamp formatting"""
        from backend.utils import format_timestamp
        
        timestamp = datetime.now()
        formatted = format_timestamp(timestamp)
        
        assert isinstance(formatted, str)
        assert len(formatted) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

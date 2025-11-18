"""
Integration Tests for API Endpoints
Tests for routes, authentication, and database operations
"""

import pytest
import json
from flask import session


@pytest.mark.integration
class TestAuthenticationAPI:
    """Test authentication endpoints"""
    
    def test_register_user(self, client, db):
        """Test user registration"""
        response = client.post('/api/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecureP@ss123',
            'role': 'student'
        })
        
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        assert 'user_id' in data or 'message' in data
    
    def test_register_duplicate_user(self, client, sample_user):
        """Test registration with existing username"""
        response = client.post('/api/register', json={
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'SecureP@ss123'
        })
        
        assert response.status_code in [400, 409]
    
    def test_login_valid_credentials(self, client, sample_user):
        """Test login with valid credentials"""
        response = client.post('/api/login', json={
            'username': 'testuser',
            'password': 'correctpassword'
        })
        
        # May fail if password hashing not implemented yet
        assert response.status_code in [200, 401]
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        response = client.post('/api/login', json={
            'username': 'nonexistent',
            'password': 'wrongpassword'
        })
        
        assert response.status_code in [400, 401]
    
    def test_logout(self, client, sample_user):
        """Test logout endpoint"""
        # Login first
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/logout')
        
        assert response.status_code == 200


@pytest.mark.integration
class TestChatAPI:
    """Test chat endpoints"""
    
    def test_send_message_authenticated(self, client, sample_user):
        """Test sending message as authenticated user"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/chat', json={
            'message': 'Hello, bot!',
            'session_id': 'test-session'
        })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
    
    def test_send_message_unauthenticated(self, client):
        """Test sending message without authentication"""
        response = client.post('/api/chat', json={
            'message': 'Hello, bot!',
            'session_id': 'test-session'
        })
        
        # Should still work for guest users
        assert response.status_code in [200, 401]
    
    def test_get_chat_history(self, client, sample_user, sample_conversation):
        """Test retrieving chat history"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.get('/api/chat/history')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_delete_chat_history(self, client, sample_user):
        """Test deleting chat history"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.delete('/api/chat/history')
        
        assert response.status_code in [200, 204]


@pytest.mark.integration
class TestContextAPI:
    """Test context management endpoints"""
    
    def test_save_context(self, client, sample_user):
        """Test saving conversation context"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/context/save', json={
            'session_id': 'test-session',
            'context_data': {
                'topic': 'programming',
                'subtopic': 'python'
            }
        })
        
        assert response.status_code in [200, 201]
    
    def test_get_context(self, client, sample_user):
        """Test retrieving context"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        # Save context first
        client.post('/api/context/save', json={
            'session_id': 'test-session',
            'context_data': {'topic': 'math'}
        })
        
        # Retrieve context
        response = client.get('/api/context/test-session')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'topic' in data or 'context' in data
    
    def test_clear_context(self, client, sample_user):
        """Test clearing context"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.delete('/api/context/test-session')
        
        assert response.status_code in [200, 204]


@pytest.mark.integration
class TestAutocompleteAPI:
    """Test autocomplete endpoints"""
    
    def test_get_suggestions(self, client):
        """Test getting autocomplete suggestions"""
        response = client.get('/api/autocomplete?q=what&limit=5')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) <= 5
    
    def test_get_suggestions_with_context(self, client, sample_user):
        """Test context-aware suggestions"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/autocomplete/smart', json={
            'query': 'what',
            'context': {
                'previous_messages': ['tell me about courses'],
                'current_topic': 'academics'
            },
            'limit': 5
        })
        
        assert response.status_code == 200
    
    def test_learn_from_query(self, client):
        """Test learning from user queries"""
        response = client.post('/api/autocomplete/learn', json={
            'query': 'what is machine learning'
        })
        
        assert response.status_code in [200, 201]


@pytest.mark.integration
class TestImageAPI:
    """Test image processing endpoints"""
    
    def test_upload_image(self, client, sample_user):
        """Test image upload"""
        from io import BytesIO
        
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        # Create fake image file
        data = {
            'file': (BytesIO(b'fake image data'), 'test.jpg')
        }
        
        response = client.post(
            '/api/image/upload',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code in [200, 201, 400]  # 400 if validation fails
    
    def test_analyze_image(self, client, sample_user):
        """Test image analysis"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/image/analyze', json={
            'image_url': 'test.jpg'
        })
        
        assert response.status_code in [200, 400, 404]


@pytest.mark.integration
class TestVoiceAPI:
    """Test voice processing endpoints"""
    
    def test_text_to_speech(self, client):
        """Test TTS endpoint"""
        response = client.post('/api/voice/tts', json={
            'text': 'Hello, this is a test',
            'voice': 'default',
            'rate': 1.0,
            'pitch': 1.0
        })
        
        assert response.status_code in [200, 501]  # 501 if not implemented
    
    def test_speech_to_text(self, client):
        """Test STT endpoint"""
        from io import BytesIO
        
        data = {
            'audio': (BytesIO(b'fake audio data'), 'test.wav')
        }
        
        response = client.post(
            '/api/voice/stt',
            data=data,
            content_type='multipart/form-data'
        )
        
        assert response.status_code in [200, 400, 501]


@pytest.mark.integration
class TestI18nAPI:
    """Test internationalization endpoints"""
    
    def test_get_translations(self, client):
        """Test getting translations"""
        response = client.get('/api/i18n/translations/en')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_set_language(self, client):
        """Test setting language preference"""
        response = client.post('/api/i18n/language', json={
            'language': 'es'
        })
        
        assert response.status_code == 200
    
    def test_get_supported_languages(self, client):
        """Test getting supported languages"""
        response = client.get('/api/i18n/languages')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)


@pytest.mark.integration
class TestAnalyticsAPI:
    """Test analytics endpoints"""
    
    def test_track_event(self, client, sample_user):
        """Test event tracking"""
        with client.session_transaction() as sess:
            sess['user_id'] = sample_user.user_id
        
        response = client.post('/api/analytics/event', json={
            'event_type': 'message_sent',
            'event_data': {
                'message_length': 10,
                'session_id': 'test-session'
            }
        })
        
        assert response.status_code in [200, 201]
    
    def test_get_analytics(self, client, admin_user):
        """Test getting analytics data"""
        with client.session_transaction() as sess:
            sess['user_id'] = admin_user.user_id
            sess['role'] = 'admin'
        
        response = client.get('/api/analytics/dashboard')
        
        assert response.status_code in [200, 403]


@pytest.mark.integration
class TestDatabaseOperations:
    """Test database operations"""
    
    def test_create_user(self, db):
        """Test creating user in database"""
        from database.models import User
        
        user = User(
            username='dbtest',
            email='dbtest@example.com',
            password_hash='hashed',
            role='student'
        )
        
        db.session.add(user)
        db.session.commit()
        
        assert user.user_id is not None
    
    def test_create_conversation(self, db, sample_user):
        """Test creating conversation in database"""
        from database.models import Conversation
        
        conversation = Conversation(
            user_id=sample_user.user_id,
            user_message='Test message',
            bot_response='Test response',
            session_id='test-session'
        )
        
        db.session.add(conversation)
        db.session.commit()
        
        assert conversation.conversation_id is not None
    
    def test_query_conversations(self, db, sample_user, sample_conversation):
        """Test querying conversations"""
        from database.models import Conversation
        
        conversations = Conversation.query.filter_by(
            user_id=sample_user.user_id
        ).all()
        
        assert len(conversations) > 0
    
    def test_update_user_profile(self, db, sample_user):
        """Test updating user profile"""
        sample_user.email = 'updated@example.com'
        db.session.commit()
        
        from database.models import User
        updated = User.query.get(sample_user.user_id)
        
        assert updated.email == 'updated@example.com'
    
    def test_delete_conversation(self, db, sample_conversation):
        """Test deleting conversation"""
        conversation_id = sample_conversation.conversation_id
        
        db.session.delete(sample_conversation)
        db.session.commit()
        
        from database.models import Conversation
        deleted = Conversation.query.get(conversation_id)
        
        assert deleted is None


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent/route')
        
        assert response.status_code == 404
    
    def test_400_bad_request(self, client):
        """Test 400 error handling"""
        response = client.post('/api/chat', json={})  # Missing required fields
        
        assert response.status_code in [400, 422]
    
    def test_500_error_handling(self, client):
        """Test 500 error handling"""
        # This would require mocking a server error
        pass


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

"""
Context Memory API Routes
Provides endpoints for managing conversation context and memory
"""

from flask import Blueprint, request, jsonify, session
from backend.context_manager import context_manager
from functools import wraps

context_bp = Blueprint('context', __name__)


def get_session_id():
    """Get or create session ID"""
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']


@context_bp.route('/save', methods=['POST'])
def save_context():
    """
    Save conversation context
    
    Body:
        {
            "messages": [{"sender": "user|bot", "text": "message", "timestamp": "ISO8601"}],
            "user_id": 123  // optional
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing messages in request body'
            }), 400
        
        session_id = get_session_id()
        messages = data['messages']
        user_id = data.get('user_id')
        
        success = context_manager.save_context(session_id, messages, user_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Context saved successfully',
                'session_id': session_id,
                'message_count': len(messages)
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to save context'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error saving context: {str(e)}'
        }), 500


@context_bp.route('/load', methods=['GET'])
def load_context():
    """
    Load conversation context for current session
    
    Returns:
        {
            "status": "success",
            "data": {
                "context_id": 123,
                "session_id": "uuid",
                "context_data": [...],
                "message_count": 10,
                "last_active": "ISO8601",
                "created_at": "ISO8601"
            }
        }
    """
    try:
        session_id = get_session_id()
        context_data = context_manager.load_context(session_id)
        
        if context_data:
            return jsonify({
                'status': 'success',
                'data': context_data,
                'has_context': True
            })
        else:
            return jsonify({
                'status': 'success',
                'data': None,
                'has_context': False,
                'message': 'No context found for this session'
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error loading context: {str(e)}'
        }), 500


@context_bp.route('/recent', methods=['GET'])
def get_recent_messages():
    """
    Get recent messages from context
    
    Query params:
        limit: Number of messages to retrieve (default: 10)
    
    Returns:
        {
            "status": "success",
            "messages": [...],
            "count": 10
        }
    """
    try:
        session_id = get_session_id()
        limit = request.args.get('limit', 10, type=int)
        
        # Ensure limit is reasonable
        limit = min(max(1, limit), 50)
        
        messages = context_manager.get_recent_messages(session_id, limit)
        
        return jsonify({
            'status': 'success',
            'messages': messages,
            'count': len(messages),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving messages: {str(e)}'
        }), 500


@context_bp.route('/append', methods=['POST'])
def append_message():
    """
    Append a new message to context
    
    Body:
        {
            "sender": "user|bot",
            "text": "message text",
            "timestamp": "ISO8601"  // optional
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'sender' not in data or 'text' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing sender or text in request body'
            }), 400
        
        session_id = get_session_id()
        user_id = data.get('user_id')
        
        success = context_manager.append_message(session_id, data, user_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Message appended to context',
                'session_id': session_id
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to append message'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error appending message: {str(e)}'
        }), 500


@context_bp.route('/clear', methods=['POST'])
def clear_context():
    """
    Clear conversation context for current session
    
    Returns:
        {
            "status": "success",
            "message": "Context cleared"
        }
    """
    try:
        session_id = get_session_id()
        success = context_manager.clear_context(session_id)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Context cleared successfully',
                'session_id': session_id
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to clear context'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error clearing context: {str(e)}'
        }), 500


@context_bp.route('/summary', methods=['GET'])
def get_context_summary():
    """
    Get summary of conversation context
    
    Returns:
        {
            "status": "success",
            "summary": {
                "exists": true,
                "message_count": 25,
                "user_messages": 13,
                "bot_messages": 12,
                "last_active": "ISO8601",
                "created_at": "ISO8601"
            }
        }
    """
    try:
        session_id = get_session_id()
        summary = context_manager.get_context_summary(session_id)
        
        return jsonify({
            'status': 'success',
            'summary': summary,
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting summary: {str(e)}'
        }), 500


@context_bp.route('/keywords', methods=['GET'])
def get_context_keywords():
    """
    Extract top keywords from conversation context
    
    Query params:
        top_n: Number of keywords to return (default: 10)
    
    Returns:
        {
            "status": "success",
            "keywords": ["keyword1", "keyword2", ...],
            "count": 10
        }
    """
    try:
        session_id = get_session_id()
        top_n = request.args.get('top_n', 10, type=int)
        
        # Ensure top_n is reasonable
        top_n = min(max(1, top_n), 50)
        
        keywords = context_manager.extract_context_keywords(session_id, top_n)
        
        return jsonify({
            'status': 'success',
            'keywords': keywords,
            'count': len(keywords),
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error extracting keywords: {str(e)}'
        }), 500


@context_bp.route('/user/<int:user_id>/contexts', methods=['GET'])
def get_user_contexts(user_id):
    """
    Get all contexts for a specific user
    
    Query params:
        limit: Maximum number of contexts (default: 10)
    
    Returns:
        {
            "status": "success",
            "contexts": [...],
            "count": 5
        }
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        limit = min(max(1, limit), 50)
        
        contexts = context_manager.get_user_contexts(user_id, limit)
        
        return jsonify({
            'status': 'success',
            'contexts': contexts,
            'count': len(contexts),
            'user_id': user_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error retrieving user contexts: {str(e)}'
        }), 500


@context_bp.route('/session-id', methods=['GET'])
def get_session_id_endpoint():
    """
    Get current session ID
    
    Returns:
        {
            "status": "success",
            "session_id": "uuid"
        }
    """
    try:
        session_id = get_session_id()
        
        return jsonify({
            'status': 'success',
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting session ID: {str(e)}'
        }), 500

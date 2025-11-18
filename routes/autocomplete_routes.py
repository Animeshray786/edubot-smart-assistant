"""
Autocomplete API Routes
Provides endpoints for smart autocomplete suggestions
"""

from flask import Blueprint, request, jsonify
from backend.autocomplete_engine import autocomplete_engine

autocomplete_bp = Blueprint('autocomplete', __name__)


@autocomplete_bp.route('/suggest', methods=['POST'])
def get_suggestions():
    """
    Get autocomplete suggestions for a query
    
    Body:
        {
            "query": "user's partial query",
            "limit": 5  // optional
        }
    
    Returns:
        {
            "status": "success",
            "suggestions": [
                {
                    "text": "suggestion text",
                    "score": 0.95,
                    "source": "popular|history|aiml",
                    "icon": "⭐"
                }
            ],
            "count": 5
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing query in request body'
            }), 400
        
        query = data['query']
        limit = data.get('limit', 5)
        
        # Ensure limit is reasonable
        limit = min(max(1, limit), 20)
        
        suggestions = autocomplete_engine.get_suggestions(query, limit)
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'count': len(suggestions)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting suggestions: {str(e)}'
        }), 500


@autocomplete_bp.route('/add-history', methods=['POST'])
def add_to_history():
    """
    Add a query to user history
    
    Body:
        {
            "query": "user's query"
        }
    
    Returns:
        {
            "status": "success",
            "message": "Query added to history"
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing query in request body'
            }), 400
        
        query = data['query']
        autocomplete_engine.add_to_history(query)
        
        return jsonify({
            'status': 'success',
            'message': 'Query added to history'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error adding to history: {str(e)}'
        }), 500


@autocomplete_bp.route('/category/<category>', methods=['GET'])
def get_category_suggestions(category):
    """
    Get suggestions for a specific category
    
    Path params:
        category: Category name (academic, study, college, features)
    
    Query params:
        limit: Number of suggestions (default: 5)
    
    Returns:
        {
            "status": "success",
            "category": "academic",
            "suggestions": ["question1", "question2", ...],
            "count": 5
        }
    """
    try:
        limit = request.args.get('limit', 5, type=int)
        limit = min(max(1, limit), 20)
        
        suggestions = autocomplete_engine.get_category_suggestions(category, limit)
        
        return jsonify({
            'status': 'success',
            'category': category,
            'suggestions': suggestions,
            'count': len(suggestions)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting category suggestions: {str(e)}'
        }), 500


@autocomplete_bp.route('/trending', methods=['GET'])
def get_trending():
    """
    Get trending queries from recent history
    
    Query params:
        limit: Number of queries (default: 5)
    
    Returns:
        {
            "status": "success",
            "trending": ["query1", "query2", ...],
            "count": 5
        }
    """
    try:
        limit = request.args.get('limit', 5, type=int)
        limit = min(max(1, limit), 20)
        
        trending = autocomplete_engine.get_trending_queries(limit)
        
        return jsonify({
            'status': 'success',
            'trending': trending,
            'count': len(trending)
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting trending queries: {str(e)}'
        }), 500


@autocomplete_bp.route('/clear-history', methods=['POST'])
def clear_history():
    """
    Clear user query history
    
    Returns:
        {
            "status": "success",
            "message": "History cleared"
        }
    """
    try:
        autocomplete_engine.clear_history()
        
        return jsonify({
            'status': 'success',
            'message': 'History cleared successfully'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error clearing history: {str(e)}'
        }), 500


@autocomplete_bp.route('/stats', methods=['GET'])
def get_stats():
    """
    Get autocomplete engine statistics
    
    Returns:
        {
            "status": "success",
            "stats": {
                "total_patterns": 100,
                "popular_questions": 40,
                "user_history_size": 25,
                "max_history": 100,
                "min_similarity": 0.6
            }
        }
    """
    try:
        stats = autocomplete_engine.get_stats()
        
        return jsonify({
            'status': 'success',
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Error getting stats: {str(e)}'
        }), 500

"""
Admin Routes for Hybrid Voice Chatbot
Admin dashboard and management endpoints
"""
from flask import Blueprint, request, session, jsonify, current_app, render_template
from database import db
from database.db_manager import DatabaseManager
from backend.utils import admin_required, success_response, error_response

admin_bp = Blueprint('admin', __name__)
db_manager = DatabaseManager(db)


@admin_bp.route('/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """Render admin dashboard"""
    return render_template('admin_dashboard.html')


@admin_bp.route('/analytics', methods=['GET'])
@admin_required
def get_analytics():
    """Get analytics data"""
    try:
        from backend.analytics import Analytics
        analytics = Analytics(db_manager)
        stats = analytics.get_dashboard_stats()
        
        return success_response(stats)
        
    except Exception as e:
        print(f"Error getting analytics: {str(e)}")
        return error_response('Failed to get analytics', 500)


@admin_bp.route('/feedback', methods=['GET'])
@admin_required
def get_all_feedback():
    """Get all feedback"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        feedback = db_manager.get_all_feedback(page, per_page)
        
        return success_response({
            'feedback': [f.to_dict() for f in feedback.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': feedback.total,
                'pages': feedback.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting feedback: {str(e)}")
        return error_response('Failed to get feedback', 500)


@admin_bp.route('/knowledge/pending', methods=['GET'])
@admin_required
def get_pending_knowledge():
    """Get pending knowledge entries"""
    try:
        pending = db_manager.get_pending_knowledge()
        
        return success_response({
            'knowledge': [k.to_dict() for k in pending]
        })
        
    except Exception as e:
        print(f"Error getting pending knowledge: {str(e)}")
        return error_response('Failed to get pending knowledge', 500)


@admin_bp.route('/knowledge/<int:kb_id>/approve', methods=['POST'])
@admin_required
def approve_knowledge(kb_id):
    """Approve a knowledge entry"""
    try:
        kb = db_manager.approve_knowledge(kb_id, session['user_id'])
        
        if not kb:
            return error_response('Knowledge entry not found', 404)
        
        # Add to AIML
        aiml_engine = current_app.aiml_engine
        from backend.learning_module import LearningModule
        learning = LearningModule(db_manager, aiml_engine)
        learning.add_to_aiml(kb.question, kb.answer)
        
        return success_response({
            'knowledge': kb.to_dict(),
            'message': 'Knowledge approved and added to AIML'
        })
        
    except Exception as e:
        print(f"Error approving knowledge: {str(e)}")
        return error_response('Failed to approve knowledge', 500)


@admin_bp.route('/knowledge/<int:kb_id>/reject', methods=['POST'])
@admin_required
def reject_knowledge(kb_id):
    """Reject a knowledge entry"""
    try:
        kb = db_manager.reject_knowledge(kb_id)
        
        if not kb:
            return error_response('Knowledge entry not found', 404)
        
        return success_response({
            'knowledge': kb.to_dict(),
            'message': 'Knowledge rejected'
        })
        
    except Exception as e:
        print(f"Error rejecting knowledge: {str(e)}")
        return error_response('Failed to reject knowledge', 500)


@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        users = db_manager.get_all_users(page, per_page)
        
        return success_response({
            'users': [u.to_dict() for u in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        return error_response('Failed to get users', 500)


@admin_bp.route('/aiml/reload', methods=['POST'])
@admin_required
def reload_aiml():
    """Reload AIML patterns"""
    try:
        aiml_engine = current_app.aiml_engine
        success = aiml_engine.reload_patterns()
        
        if success:
            return success_response({
                'pattern_count': aiml_engine.get_pattern_count(),
                'message': 'AIML patterns reloaded successfully'
            })
        else:
            return error_response('Failed to reload AIML patterns', 500)
            
    except Exception as e:
        print(f"Error reloading AIML: {str(e)}")
        return error_response('Failed to reload AIML', 500)

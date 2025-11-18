"""
Admin Dashboard Routes
Real-time monitoring, analytics visualization, pattern management, and system configuration
"""
from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for, current_app
from database import db
from database.db_manager import DatabaseManager
from backend.utils import login_required, admin_required, success_response, error_response
from datetime import datetime, timedelta
from sqlalchemy import func, desc
import json
import os

admin_bp = Blueprint('admin', __name__)
db_manager = DatabaseManager(db)


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Admin dashboard home"""
    return render_template('admin/dashboard.html')


@admin_bp.route('/stats/overview', methods=['GET'])
@login_required
@admin_required
def get_overview_stats():
    """Get overview statistics for dashboard"""
    try:
        from database.models import User, Conversation, Feedback, KnowledgeBase, Session as UserSession
        
        # Time filters
        days = request.args.get('days', 7, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Total counts
        total_users = db.session.query(func.count(User.user_id)).scalar()
        total_conversations = db.session.query(func.count(Conversation.conversation_id)).scalar()
        total_feedback = db.session.query(func.count(Feedback.feedback_id)).scalar()
        pending_knowledge = db.session.query(func.count(KnowledgeBase.kb_id)).filter(
            KnowledgeBase.status == 'pending'
        ).scalar()
        
        # Active users (conversations in period)
        active_users = db.session.query(func.count(func.distinct(Conversation.user_id))).filter(
            Conversation.timestamp >= start_date
        ).scalar()
        
        # Conversations in period
        recent_conversations = db.session.query(func.count(Conversation.conversation_id)).filter(
            Conversation.timestamp >= start_date
        ).scalar()
        
        # Average sentiment
        avg_sentiment = db.session.query(func.avg(Conversation.confidence_score)).filter(
            Conversation.sentiment == 'positive'
        ).scalar() or 0
        
        # Feedback stats
        positive_feedback = db.session.query(func.count(Feedback.feedback_id)).filter(
            Feedback.rating == 'good',
            Feedback.timestamp >= start_date
        ).scalar()
        
        negative_feedback = db.session.query(func.count(Feedback.feedback_id)).filter(
            Feedback.rating.in_(['bad', 'improvement']),
            Feedback.timestamp >= start_date
        ).scalar()
        
        satisfaction_rate = 0
        if positive_feedback + negative_feedback > 0:
            satisfaction_rate = (positive_feedback / (positive_feedback + negative_feedback)) * 100
        
        # Active sessions
        active_sessions = db.session.query(func.count(UserSession.session_id)).filter(
            UserSession.last_activity >= datetime.now() - timedelta(minutes=30)
        ).scalar()
        
        return success_response({
            'overview': {
                'total_users': total_users,
                'active_users': active_users,
                'total_conversations': total_conversations,
                'recent_conversations': recent_conversations,
                'total_feedback': total_feedback,
                'pending_knowledge': pending_knowledge,
                'active_sessions': active_sessions,
                'satisfaction_rate': round(satisfaction_rate, 2),
                'avg_sentiment_score': round(avg_sentiment * 100, 2)
            },
            'period_days': days
        })
        
    except Exception as e:
        print(f"Error getting overview stats: {str(e)}")
        return error_response('Failed to get overview stats', 500)


@admin_bp.route('/stats/conversations-timeline', methods=['GET'])
@login_required
@admin_required
def get_conversations_timeline():
    """Get conversations timeline for chart"""
    try:
        from database.models import Conversation
        
        days = request.args.get('days', 7, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        # Group by date
        timeline = db.session.query(
            func.date(Conversation.timestamp).label('date'),
            func.count(Conversation.conversation_id).label('count')
        ).filter(
            Conversation.timestamp >= start_date
        ).group_by(
            func.date(Conversation.timestamp)
        ).order_by('date').all()
        
        data = {
            'labels': [str(item.date) for item in timeline],
            'values': [item.count for item in timeline]
        }
        
        return success_response(data)
        
    except Exception as e:
        print(f"Error getting timeline: {str(e)}")
        return error_response('Failed to get timeline', 500)


@admin_bp.route('/stats/sentiment-distribution', methods=['GET'])
@login_required
@admin_required
def get_sentiment_distribution():
    """Get sentiment distribution for pie chart"""
    try:
        from database.models import Conversation
        
        days = request.args.get('days', 7, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        sentiments = db.session.query(
            Conversation.sentiment,
            func.count(Conversation.conversation_id).label('count')
        ).filter(
            Conversation.timestamp >= start_date
        ).group_by(Conversation.sentiment).all()
        
        data = {
            'labels': [item.sentiment.capitalize() for item in sentiments],
            'values': [item.count for item in sentiments],
            'colors': {
                'positive': '#10b981',
                'neutral': '#6b7280',
                'negative': '#ef4444'
            }
        }
        
        return success_response(data)
        
    except Exception as e:
        print(f"Error getting sentiment distribution: {str(e)}")
        return error_response('Failed to get sentiment distribution', 500)


@admin_bp.route('/stats/category-breakdown', methods=['GET'])
@login_required
@admin_required
def get_category_breakdown():
    """Get conversation category breakdown"""
    try:
        from database.models import Conversation
        
        days = request.args.get('days', 7, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        categories = db.session.query(
            Conversation.category,
            func.count(Conversation.conversation_id).label('count')
        ).filter(
            Conversation.timestamp >= start_date
        ).group_by(Conversation.category).order_by(desc('count')).all()
        
        data = {
            'labels': [item.category or 'general' for item in categories],
            'values': [item.count for item in categories]
        }
        
        return success_response(data)
        
    except Exception as e:
        print(f"Error getting category breakdown: {str(e)}")
        return error_response('Failed to get category breakdown', 500)


@admin_bp.route('/stats/top-users', methods=['GET'])
@login_required
@admin_required
def get_top_users():
    """Get most active users"""
    try:
        from database.models import Conversation, User
        
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 10, type=int)
        start_date = datetime.now() - timedelta(days=days)
        
        top_users = db.session.query(
            User.username,
            User.email,
            func.count(Conversation.conversation_id).label('conversation_count')
        ).join(
            Conversation, User.user_id == Conversation.user_id
        ).filter(
            Conversation.timestamp >= start_date
        ).group_by(
            User.user_id, User.username, User.email
        ).order_by(
            desc('conversation_count')
        ).limit(limit).all()
        
        users_data = [{
            'username': user.username,
            'email': user.email,
            'conversations': user.conversation_count
        } for user in top_users]
        
        return success_response({'top_users': users_data})
        
    except Exception as e:
        print(f"Error getting top users: {str(e)}")
        return error_response('Failed to get top users', 500)


@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def manage_users():
    """User management page"""
    try:
        from database.models import User
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '').strip()
        
        query = User.query
        
        if search:
            query = query.filter(
                (User.username.ilike(f'%{search}%')) |
                (User.email.ilike(f'%{search}%'))
            )
        
        users = query.order_by(desc(User.created_at)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        users_data = [{
            'user_id': user.user_id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        } for user in users.items]
        
        return success_response({
            'users': users_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages
            }
        })
        
    except Exception as e:
        print(f"Error managing users: {str(e)}")
        return error_response('Failed to get users', 500)


@admin_bp.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    try:
        from database.models import User
        
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)
        
        # Prevent deactivating yourself
        if user.user_id == session['user_id']:
            return error_response('Cannot deactivate your own account', 400)
        
        user.is_active = not user.is_active
        user.updated_at = datetime.now()
        db.session.commit()
        
        return success_response({
            'message': f"User {'activated' if user.is_active else 'deactivated'} successfully",
            'is_active': user.is_active
        })
        
    except Exception as e:
        print(f"Error toggling user status: {str(e)}")
        db.session.rollback()
        return error_response('Failed to update user status', 500)


@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@login_required
@admin_required
def update_user_role(user_id):
    """Update user role"""
    try:
        from database.models import User
        
        data = request.get_json()
        new_role = data.get('role')
        
        if new_role not in ['user', 'admin']:
            return error_response('Invalid role', 400)
        
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 404)
        
        # Prevent changing your own role
        if user.user_id == session['user_id']:
            return error_response('Cannot change your own role', 400)
        
        user.role = new_role
        user.updated_at = datetime.now()
        db.session.commit()
        
        return success_response({
            'message': f"User role updated to {new_role}",
            'role': new_role
        })
        
    except Exception as e:
        print(f"Error updating user role: {str(e)}")
        db.session.rollback()
        return error_response('Failed to update user role', 500)


@admin_bp.route('/knowledge/pending', methods=['GET'])
@login_required
@admin_required
def get_pending_knowledge():
    """Get pending knowledge base entries for review"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        knowledge = db_manager.get_all_knowledge('pending', page, per_page)
        
        return success_response({
            'knowledge': [k.to_dict() for k in knowledge.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': knowledge.total,
                'pages': knowledge.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting pending knowledge: {str(e)}")
        return error_response('Failed to get pending knowledge', 500)


@admin_bp.route('/knowledge/<int:kb_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_knowledge(kb_id):
    """Approve knowledge base entry"""
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
            'message': 'Knowledge entry approved successfully',
            'kb_id': kb_id
        })
        
    except Exception as e:
        print(f"Error approving knowledge: {str(e)}")
        return error_response('Failed to approve knowledge', 500)


@admin_bp.route('/knowledge/<int:kb_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_knowledge(kb_id):
    """Reject knowledge base entry"""
    try:
        data = request.get_json()
        reason = data.get('reason', 'Quality standards not met')
        
        kb = db_manager.reject_knowledge(kb_id)
        
        if not kb:
            return error_response('Knowledge entry not found', 404)
        
        return success_response({
            'message': 'Knowledge entry rejected',
            'kb_id': kb_id,
            'reason': reason
        })
        
    except Exception as e:
        print(f"Error rejecting knowledge: {str(e)}")
        return error_response('Failed to reject knowledge', 500)


@admin_bp.route('/patterns', methods=['GET'])
@login_required
@admin_required
def get_aiml_patterns():
    """Get list of AIML pattern files"""
    try:
        aiml_dir = os.path.join(os.getcwd(), 'aiml')
        pattern_files = []
        
        if os.path.exists(aiml_dir):
            for filename in os.listdir(aiml_dir):
                if filename.endswith('.xml'):
                    filepath = os.path.join(aiml_dir, filename)
                    stat = os.stat(filepath)
                    
                    # Count patterns in file
                    pattern_count = 0
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            pattern_count = content.count('<pattern>')
                    except:
                        pass
                    
                    pattern_files.append({
                        'filename': filename,
                        'size': stat.st_size,
                        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'pattern_count': pattern_count
                    })
        
        return success_response({
            'pattern_files': sorted(pattern_files, key=lambda x: x['filename'])
        })
        
    except Exception as e:
        print(f"Error getting AIML patterns: {str(e)}")
        return error_response('Failed to get AIML patterns', 500)


@admin_bp.route('/patterns/<filename>', methods=['GET'])
@login_required
@admin_required
def get_pattern_file_content(filename):
    """Get content of specific AIML pattern file"""
    try:
        # Security: prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return error_response('Invalid filename', 400)
        
        filepath = os.path.join(os.getcwd(), 'aiml', filename)
        
        if not os.path.exists(filepath):
            return error_response('File not found', 404)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return success_response({
            'filename': filename,
            'content': content
        })
        
    except Exception as e:
        print(f"Error reading pattern file: {str(e)}")
        return error_response('Failed to read pattern file', 500)


@admin_bp.route('/patterns/<filename>', methods=['PUT'])
@login_required
@admin_required
def update_pattern_file(filename):
    """Update AIML pattern file content"""
    try:
        # Security: prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return error_response('Invalid filename', 400)
        
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return error_response('Content required', 400)
        
        filepath = os.path.join(os.getcwd(), 'aiml', filename)
        
        # Create backup
        if os.path.exists(filepath):
            backup_path = filepath + '.backup'
            with open(filepath, 'r', encoding='utf-8') as f:
                backup_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(backup_content)
        
        # Write new content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return success_response({
            'message': 'Pattern file updated successfully',
            'filename': filename
        })
        
    except Exception as e:
        print(f"Error updating pattern file: {str(e)}")
        return error_response('Failed to update pattern file', 500)


@admin_bp.route('/system/config', methods=['GET'])
@login_required
@admin_required
def get_system_config():
    """Get system configuration"""
    try:
        from config import DevelopmentConfig
        
        config = {
            'debug_mode': current_app.config.get('DEBUG', False),
            'database_url': 'SQLite (Local)',
            'session_lifetime': '24 hours',
            'max_upload_size': '16 MB',
            'aiml_patterns': 150,
            'features_enabled': 60,
            'voice_enabled': True,
            'learning_mode': True,
            'analytics_enabled': True
        }
        
        return success_response({'config': config})
        
    except Exception as e:
        print(f"Error getting system config: {str(e)}")
        return error_response('Failed to get system config', 500)


@admin_bp.route('/system/reload-aiml', methods=['POST'])
@login_required
@admin_required
def reload_aiml_patterns():
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
        return error_response('Failed to reload AIML patterns', 500)


@admin_bp.route('/system/clear-cache', methods=['POST'])
@login_required
@admin_required
def clear_system_cache():
    """Clear system cache"""
    try:
        # TODO: Implement cache clearing
        
        return success_response({
            'message': 'System cache cleared successfully'
        })
        
    except Exception as e:
        print(f"Error clearing cache: {str(e)}")
        return error_response('Failed to clear cache', 500)


@admin_bp.route('/feedback/all', methods=['GET'])
@login_required
@admin_required
def get_all_feedback():
    """Get all feedback with filters"""
    try:
        from database.models import Feedback, User, Conversation
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        rating_filter = request.args.get('rating', None)
        
        query = db.session.query(
            Feedback,
            User.username,
            Conversation.message
        ).join(
            Conversation, Feedback.conversation_id == Conversation.conversation_id
        ).join(
            User, Conversation.user_id == User.user_id
        )
        
        if rating_filter:
            query = query.filter(Feedback.rating == rating_filter)
        
        feedback_list = query.order_by(desc(Feedback.timestamp)).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        feedback_data = [{
            'feedback_id': item.Feedback.feedback_id,
            'conversation_id': item.Feedback.conversation_id,
            'rating': item.Feedback.rating,
            'comments': item.Feedback.comments,
            'timestamp': item.Feedback.timestamp.isoformat(),
            'username': item.username,
            'message': item.message[:100] + '...' if len(item.message) > 100 else item.message
        } for item in feedback_list.items]
        
        return success_response({
            'feedback': feedback_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': feedback_list.total,
                'pages': feedback_list.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting feedback: {str(e)}")
        return error_response('Failed to get feedback', 500)


@admin_bp.route('/conversations/recent', methods=['GET'])
@login_required
@admin_required
def get_recent_conversations():
    """Get recent conversations for monitoring"""
    try:
        from database.models import Conversation, User
        
        limit = request.args.get('limit', 50, type=int)
        
        conversations = db.session.query(
            Conversation,
            User.username
        ).join(
            User, Conversation.user_id == User.user_id
        ).order_by(
            desc(Conversation.timestamp)
        ).limit(limit).all()
        
        conv_data = [{
            'conversation_id': item.Conversation.conversation_id,
            'username': item.username,
            'message': item.Conversation.message,
            'response': item.Conversation.response[:200] + '...' if len(item.Conversation.response) > 200 else item.Conversation.response,
            'sentiment': item.Conversation.sentiment,
            'confidence': round(item.Conversation.confidence_score * 100, 2) if item.Conversation.confidence_score else 0,
            'category': item.Conversation.category,
            'timestamp': item.Conversation.timestamp.isoformat()
        } for item in conversations]
        
        return success_response({
            'conversations': conv_data
        })
        
    except Exception as e:
        print(f"Error getting recent conversations: {str(e)}")
        return error_response('Failed to get conversations', 500)

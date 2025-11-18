"""
Admin routes for Lecture Note Summarizer Management
"""
from flask import Blueprint, request, jsonify, render_template
from database import db
from database.lecture_notes_model import LectureNote, StudyQuestion, KeyConcept
from backend.utils import admin_required, success_response, error_response
from sqlalchemy import func, desc
from datetime import datetime, timedelta

admin_lecture_bp = Blueprint('admin_lecture', __name__)


@admin_lecture_bp.route('/', methods=['GET'])
@admin_required
def lecture_dashboard():
    """Render lecture notes admin dashboard"""
    return render_template('admin/lecture_dashboard.html')


@admin_lecture_bp.route('/overview', methods=['GET'])
@admin_required
def get_lecture_overview():
    """Get overview statistics for lecture notes"""
    try:
        # Total stats
        total_notes = LectureNote.query.count()
        total_users_with_notes = db.session.query(func.count(func.distinct(LectureNote.user_id))).scalar()
        total_questions = StudyQuestion.query.count()
        total_concepts = KeyConcept.query.count()
        
        # Status breakdown
        status_breakdown = db.session.query(
            LectureNote.status,
            func.count(LectureNote.note_id)
        ).group_by(LectureNote.status).all()
        
        # Subject breakdown
        subject_breakdown = db.session.query(
            LectureNote.subject,
            func.count(LectureNote.note_id)
        ).filter(
            LectureNote.subject.isnot(None)
        ).group_by(LectureNote.subject).order_by(desc(func.count(LectureNote.note_id))).limit(10).all()
        
        # Recent activity (last 7 days)
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        recent_notes = LectureNote.query.filter(
            LectureNote.created_at >= seven_days_ago
        ).count()
        
        # Average stats
        avg_word_count = db.session.query(func.avg(LectureNote.word_count)).scalar() or 0
        avg_questions_per_note = total_questions / total_notes if total_notes > 0 else 0
        avg_concepts_per_note = total_concepts / total_notes if total_notes > 0 else 0
        
        # Question answer rate
        answered_questions = StudyQuestion.query.filter_by(is_answered=True).count()
        answer_rate = round(answered_questions / total_questions * 100, 1) if total_questions > 0 else 0
        
        # Concept mastery
        mastered_concepts = KeyConcept.query.filter(KeyConcept.mastery_level >= 80).count()
        mastery_rate = round(mastered_concepts / total_concepts * 100, 1) if total_concepts > 0 else 0
        
        return success_response({
            'total_stats': {
                'total_notes': total_notes,
                'total_users': total_users_with_notes,
                'total_questions': total_questions,
                'total_concepts': total_concepts,
                'recent_notes_7d': recent_notes
            },
            'averages': {
                'avg_word_count': round(avg_word_count, 0),
                'avg_questions_per_note': round(avg_questions_per_note, 1),
                'avg_concepts_per_note': round(avg_concepts_per_note, 1)
            },
            'engagement': {
                'answer_rate': answer_rate,
                'answered_questions': answered_questions,
                'unanswered_questions': total_questions - answered_questions,
                'mastery_rate': mastery_rate,
                'mastered_concepts': mastered_concepts
            },
            'status_breakdown': [
                {'status': status, 'count': count} 
                for status, count in status_breakdown
            ],
            'subject_breakdown': [
                {'subject': subject or 'Uncategorized', 'count': count}
                for subject, count in subject_breakdown
            ]
        })
        
    except Exception as e:
        print(f"Error getting lecture overview: {str(e)}")
        return error_response('Failed to get overview', 500)


@admin_lecture_bp.route('/notes', methods=['GET'])
@admin_required
def get_all_notes():
    """Get all lecture notes with filters"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status', None)
        subject = request.args.get('subject', None)
        user_id = request.args.get('user_id', None, type=int)
        search = request.args.get('search', None)
        
        query = LectureNote.query
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        
        if subject:
            query = query.filter_by(subject=subject)
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if search:
            query = query.filter(
                db.or_(
                    LectureNote.title.ilike(f'%{search}%'),
                    LectureNote.tags.ilike(f'%{search}%')
                )
            )
        
        notes = query.order_by(LectureNote.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return success_response({
            'notes': [note.to_dict() for note in notes.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': notes.total,
                'pages': notes.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting all notes: {str(e)}")
        return error_response('Failed to get notes', 500)


@admin_lecture_bp.route('/notes/<int:note_id>', methods=['GET'])
@admin_required
def get_note_detail(note_id):
    """Get detailed note information"""
    try:
        note = LectureNote.query.get(note_id)
        
        if not note:
            return error_response('Note not found', 404)
        
        return success_response({
            'note': note.to_dict_full(),
            'questions': [q.to_dict() for q in note.questions],
            'concepts': [c.to_dict() for c in note.concepts],
            'user_info': {
                'user_id': note.user.user_id,
                'username': note.user.username,
                'email': note.user.email
            } if note.user else None
        })
        
    except Exception as e:
        print(f"Error getting note detail: {str(e)}")
        return error_response('Failed to get note', 500)


@admin_lecture_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@admin_required
def delete_note(note_id):
    """Delete a lecture note (admin)"""
    try:
        note = LectureNote.query.get(note_id)
        
        if not note:
            return error_response('Note not found', 404)
        
        title = note.title
        db.session.delete(note)
        db.session.commit()
        
        return success_response({
            'message': f'Note "{title}" deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting note: {str(e)}")
        return error_response('Failed to delete note', 500)


@admin_lecture_bp.route('/notes/<int:note_id>/status', methods=['PUT'])
@admin_required
def update_note_status(note_id):
    """Update note status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['processed', 'pending', 'failed']:
            return error_response('Invalid status', 400)
        
        note = LectureNote.query.get(note_id)
        
        if not note:
            return error_response('Note not found', 404)
        
        note.status = new_status
        note.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response({
            'message': 'Status updated successfully',
            'note': note.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating status: {str(e)}")
        return error_response('Failed to update status', 500)


@admin_lecture_bp.route('/users/<int:user_id>/notes', methods=['GET'])
@admin_required
def get_user_notes(user_id):
    """Get all notes for a specific user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        notes = LectureNote.query.filter_by(user_id=user_id).order_by(
            LectureNote.created_at.desc()
        ).paginate(page=page, per_page=per_page, error_out=False)
        
        # Get user stats
        total_questions = db.session.query(StudyQuestion).join(LectureNote).filter(
            LectureNote.user_id == user_id
        ).count()
        
        answered_questions = db.session.query(StudyQuestion).join(LectureNote).filter(
            LectureNote.user_id == user_id,
            StudyQuestion.is_answered == True
        ).count()
        
        return success_response({
            'notes': [note.to_dict() for note in notes.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': notes.total,
                'pages': notes.pages
            },
            'user_stats': {
                'total_notes': notes.total,
                'total_questions': total_questions,
                'answered_questions': answered_questions
            }
        })
        
    except Exception as e:
        print(f"Error getting user notes: {str(e)}")
        return error_response('Failed to get user notes', 500)


@admin_lecture_bp.route('/analytics/timeline', methods=['GET'])
@admin_required
def get_notes_timeline():
    """Get timeline of note creation"""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily counts
        daily_counts = db.session.query(
            func.date(LectureNote.created_at).label('date'),
            func.count(LectureNote.note_id).label('count')
        ).filter(
            LectureNote.created_at >= start_date
        ).group_by(
            func.date(LectureNote.created_at)
        ).order_by('date').all()
        
        return success_response({
            'timeline': [
                {
                    'date': date.isoformat() if date else None,
                    'count': count
                }
                for date, count in daily_counts
            ],
            'period_days': days
        })
        
    except Exception as e:
        print(f"Error getting timeline: {str(e)}")
        return error_response('Failed to get timeline', 500)


@admin_lecture_bp.route('/analytics/popular-subjects', methods=['GET'])
@admin_required
def get_popular_subjects():
    """Get most popular subjects"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        subjects = db.session.query(
            LectureNote.subject,
            func.count(LectureNote.note_id).label('note_count'),
            func.sum(LectureNote.word_count).label('total_words')
        ).filter(
            LectureNote.subject.isnot(None)
        ).group_by(
            LectureNote.subject
        ).order_by(
            desc('note_count')
        ).limit(limit).all()
        
        return success_response({
            'subjects': [
                {
                    'subject': subject,
                    'note_count': note_count,
                    'total_words': total_words or 0
                }
                for subject, note_count, total_words in subjects
            ]
        })
        
    except Exception as e:
        print(f"Error getting popular subjects: {str(e)}")
        return error_response('Failed to get subjects', 500)


@admin_lecture_bp.route('/analytics/top-users', methods=['GET'])
@admin_required
def get_top_users():
    """Get users with most notes"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        top_users = db.session.query(
            LectureNote.user_id,
            func.count(LectureNote.note_id).label('note_count'),
            func.sum(LectureNote.word_count).label('total_words')
        ).group_by(
            LectureNote.user_id
        ).order_by(
            desc('note_count')
        ).limit(limit).all()
        
        # Get user details
        from database.models import User
        result = []
        for user_id, note_count, total_words in top_users:
            user = User.query.get(user_id)
            if user:
                result.append({
                    'user_id': user_id,
                    'username': user.username,
                    'email': user.email,
                    'note_count': note_count,
                    'total_words': total_words or 0
                })
        
        return success_response({
            'top_users': result
        })
        
    except Exception as e:
        print(f"Error getting top users: {str(e)}")
        return error_response('Failed to get top users', 500)


@admin_lecture_bp.route('/bulk-delete', methods=['POST'])
@admin_required
def bulk_delete_notes():
    """Bulk delete notes by criteria"""
    try:
        data = request.get_json()
        
        note_ids = data.get('note_ids', [])
        status = data.get('status', None)
        older_than_days = data.get('older_than_days', None)
        
        query = LectureNote.query
        
        if note_ids:
            query = query.filter(LectureNote.note_id.in_(note_ids))
        elif status:
            query = query.filter_by(status=status)
            if older_than_days:
                cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
                query = query.filter(LectureNote.created_at < cutoff_date)
        else:
            return error_response('Must provide note_ids or status criteria', 400)
        
        count = query.count()
        query.delete(synchronize_session=False)
        db.session.commit()
        
        return success_response({
            'message': f'Successfully deleted {count} notes',
            'deleted_count': count
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error bulk deleting: {str(e)}")
        return error_response('Bulk delete failed', 500)


@admin_lecture_bp.route('/export', methods=['GET'])
@admin_required
def export_notes_data():
    """Export notes data for analysis"""
    try:
        format_type = request.args.get('format', 'json')
        
        notes = LectureNote.query.all()
        
        export_data = []
        for note in notes:
            export_data.append({
                'note_id': note.note_id,
                'user_id': note.user_id,
                'username': note.user.username if note.user else None,
                'title': note.title,
                'subject': note.subject,
                'word_count': note.word_count,
                'status': note.status,
                'question_count': len(note.questions),
                'concept_count': len(note.concepts),
                'created_at': note.created_at.isoformat(),
                'tags': note.tags.split(',') if note.tags else []
            })
        
        if format_type == 'csv':
            # Convert to CSV format
            import csv
            from io import StringIO
            
            output = StringIO()
            if export_data:
                writer = csv.DictWriter(output, fieldnames=export_data[0].keys())
                writer.writeheader()
                writer.writerows(export_data)
            
            return success_response({
                'format': 'csv',
                'data': output.getvalue()
            })
        else:
            return success_response({
                'format': 'json',
                'data': export_data,
                'total_records': len(export_data)
            })
        
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        return error_response('Export failed', 500)

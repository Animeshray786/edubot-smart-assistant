"""
Routes for Lecture Note Summarizer
"""
from flask import Blueprint, request, session, jsonify
from database import db
from database.lecture_notes_model import LectureNote, StudyQuestion, KeyConcept
from backend.utils import login_required, success_response, error_response
from backend.lecture_summarizer import LectureSummarizer
from datetime import datetime

lecture_bp = Blueprint('lecture', __name__)
summarizer = LectureSummarizer()


@lecture_bp.route('/upload', methods=['POST'])
@login_required
def upload_lecture():
    """Upload and summarize lecture notes"""
    try:
        data = request.get_json()
        
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        subject = data.get('subject', '').strip()
        tags = data.get('tags', '')
        
        if not title:
            return error_response('Title is required', 400)
        
        if not content:
            return error_response('Content is required', 400)
        
        if len(content) < 50:
            return error_response('Content too short. Minimum 50 characters required.', 400)
        
        # Generate summary
        summary_result = summarizer.summarize_lecture(content, title)
        
        if not summary_result.get('success'):
            return error_response(summary_result.get('error', 'Summarization failed'), 400)
        
        # Save to database
        lecture_note = LectureNote(
            user_id=session['user_id'],
            title=title,
            original_content=content,
            summary_data=summary_result,
            subject=subject,
            tags=tags,
            word_count=len(content.split()),
            status='processed'
        )
        
        db.session.add(lecture_note)
        db.session.flush()  # Get note_id
        
        # Save study questions
        for question_data in summary_result['study_questions']:
            question = StudyQuestion(
                note_id=lecture_note.note_id,
                question_text=question_data['question'],
                question_type=question_data['type'],
                difficulty=question_data['difficulty'],
                related_concept=question_data['related_concept']
            )
            db.session.add(question)
        
        # Save key concepts
        for concept_data in summary_result['key_concepts']:
            concept = KeyConcept(
                note_id=lecture_note.note_id,
                term=concept_data['term'],
                definition=concept_data['definition'],
                importance=concept_data['importance']
            )
            db.session.add(concept)
        
        db.session.commit()
        
        # Generate HTML summary
        html_summary = summarizer.format_summary_html(summary_result)
        
        return success_response({
            'note_id': lecture_note.note_id,
            'title': title,
            'summary': summary_result,
            'html_summary': html_summary,
            'message': 'Lecture notes processed successfully!'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error uploading lecture: {str(e)}")
        return error_response(f'Upload failed: {str(e)}', 500)


@lecture_bp.route('/notes', methods=['GET'])
@login_required
def get_user_notes():
    """Get all lecture notes for current user"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        subject = request.args.get('subject', None)
        
        query = LectureNote.query.filter_by(user_id=session['user_id'])
        
        if subject:
            query = query.filter_by(subject=subject)
        
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
        print(f"Error getting notes: {str(e)}")
        return error_response('Failed to get notes', 500)


@lecture_bp.route('/notes/<int:note_id>', methods=['GET'])
@login_required
def get_note_detail(note_id):
    """Get detailed lecture note with full content"""
    try:
        note = LectureNote.query.filter_by(
            note_id=note_id,
            user_id=session['user_id']
        ).first()
        
        if not note:
            return error_response('Note not found', 404)
        
        # Generate fresh HTML
        html_summary = summarizer.format_summary_html(note.summary_data)
        
        return success_response({
            'note': note.to_dict_full(),
            'html_summary': html_summary,
            'questions': [q.to_dict() for q in note.questions],
            'concepts': [c.to_dict() for c in note.concepts]
        })
        
    except Exception as e:
        print(f"Error getting note detail: {str(e)}")
        return error_response('Failed to get note', 500)


@lecture_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete a lecture note"""
    try:
        note = LectureNote.query.filter_by(
            note_id=note_id,
            user_id=session['user_id']
        ).first()
        
        if not note:
            return error_response('Note not found', 404)
        
        db.session.delete(note)
        db.session.commit()
        
        return success_response({
            'message': 'Note deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deleting note: {str(e)}")
        return error_response('Failed to delete note', 500)


@lecture_bp.route('/questions/<int:question_id>/answer', methods=['POST'])
@login_required
def answer_question(question_id):
    """Submit answer to a study question"""
    try:
        data = request.get_json()
        answer = data.get('answer', '').strip()
        
        if not answer:
            return error_response('Answer is required', 400)
        
        question = StudyQuestion.query.get(question_id)
        
        if not question:
            return error_response('Question not found', 404)
        
        # Verify user owns the note
        note = LectureNote.query.get(question.note_id)
        if not note or note.user_id != session['user_id']:
            return error_response('Unauthorized', 403)
        
        question.user_answer = answer
        question.is_answered = True
        question.answered_at = datetime.utcnow()
        
        db.session.commit()
        
        return success_response({
            'message': 'Answer submitted successfully',
            'question': question.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error submitting answer: {str(e)}")
        return error_response('Failed to submit answer', 500)


@lecture_bp.route('/concepts/<int:concept_id>/review', methods=['POST'])
@login_required
def review_concept(concept_id):
    """Mark concept as reviewed and update mastery"""
    try:
        data = request.get_json()
        mastery_level = data.get('mastery_level', 0)
        
        concept = KeyConcept.query.get(concept_id)
        
        if not concept:
            return error_response('Concept not found', 404)
        
        # Verify user owns the note
        note = LectureNote.query.get(concept.note_id)
        if not note or note.user_id != session['user_id']:
            return error_response('Unauthorized', 403)
        
        concept.times_reviewed += 1
        concept.last_reviewed = datetime.utcnow()
        
        if mastery_level:
            concept.mastery_level = min(100, mastery_level)
        
        db.session.commit()
        
        return success_response({
            'message': 'Concept reviewed',
            'concept': concept.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error reviewing concept: {str(e)}")
        return error_response('Failed to review concept', 500)


@lecture_bp.route('/stats', methods=['GET'])
@login_required
def get_lecture_stats():
    """Get user's lecture note statistics"""
    try:
        total_notes = LectureNote.query.filter_by(user_id=session['user_id']).count()
        
        total_questions = db.session.query(StudyQuestion).join(LectureNote).filter(
            LectureNote.user_id == session['user_id']
        ).count()
        
        answered_questions = db.session.query(StudyQuestion).join(LectureNote).filter(
            LectureNote.user_id == session['user_id'],
            StudyQuestion.is_answered == True
        ).count()
        
        total_concepts = db.session.query(KeyConcept).join(LectureNote).filter(
            LectureNote.user_id == session['user_id']
        ).count()
        
        mastered_concepts = db.session.query(KeyConcept).join(LectureNote).filter(
            LectureNote.user_id == session['user_id'],
            KeyConcept.mastery_level >= 80
        ).count()
        
        # Get subjects
        subjects = db.session.query(LectureNote.subject, db.func.count(LectureNote.note_id)).filter(
            LectureNote.user_id == session['user_id'],
            LectureNote.subject.isnot(None)
        ).group_by(LectureNote.subject).all()
        
        return success_response({
            'total_notes': total_notes,
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'unanswered_questions': total_questions - answered_questions,
            'total_concepts': total_concepts,
            'mastered_concepts': mastered_concepts,
            'mastery_percentage': round(mastered_concepts / total_concepts * 100, 1) if total_concepts > 0 else 0,
            'subjects': [{'subject': s[0], 'count': s[1]} for s in subjects]
        })
        
    except Exception as e:
        print(f"Error getting stats: {str(e)}")
        return error_response('Failed to get statistics', 500)

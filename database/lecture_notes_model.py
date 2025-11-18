"""
Database models for Lecture Note Summarizer
"""
from database import db
from datetime import datetime


class LectureNote(db.Model):
    """Model for storing lecture notes and summaries"""
    __tablename__ = 'lecture_notes'
    
    note_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    original_content = db.Column(db.Text, nullable=False)
    summary_data = db.Column(db.JSON)  # Stores full summary JSON
    subject = db.Column(db.String(100))
    tags = db.Column(db.String(500))  # Comma-separated tags
    word_count = db.Column(db.Integer)
    status = db.Column(db.String(20), default='processed')  # processed, pending, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='lecture_notes')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'note_id': self.note_id,
            'user_id': self.user_id,
            'title': self.title,
            'original_content': self.original_content[:500] + '...' if len(self.original_content) > 500 else self.original_content,
            'summary_data': self.summary_data,
            'subject': self.subject,
            'tags': self.tags.split(',') if self.tags else [],
            'word_count': self.word_count,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def to_dict_full(self):
        """Convert to dictionary with full content"""
        data = self.to_dict()
        data['original_content'] = self.original_content
        return data


class StudyQuestion(db.Model):
    """Model for storing study questions from lectures"""
    __tablename__ = 'study_questions'
    
    question_id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('lecture_notes.note_id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50))  # short_answer, essay, list, mcq
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    related_concept = db.Column(db.String(200))
    user_answer = db.Column(db.Text)
    is_answered = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answered_at = db.Column(db.DateTime)
    
    # Relationships
    lecture_note = db.relationship('LectureNote', backref='questions')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'question_id': self.question_id,
            'note_id': self.note_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'difficulty': self.difficulty,
            'related_concept': self.related_concept,
            'user_answer': self.user_answer,
            'is_answered': self.is_answered,
            'created_at': self.created_at.isoformat(),
            'answered_at': self.answered_at.isoformat() if self.answered_at else None
        }


class KeyConcept(db.Model):
    """Model for storing key concepts from lectures"""
    __tablename__ = 'key_concepts'
    
    concept_id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('lecture_notes.note_id'), nullable=False)
    term = db.Column(db.String(200), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    importance = db.Column(db.String(20))  # high, medium, low
    mastery_level = db.Column(db.Integer, default=0)  # 0-100
    times_reviewed = db.Column(db.Integer, default=0)
    last_reviewed = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lecture_note = db.relationship('LectureNote', backref='concepts')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'concept_id': self.concept_id,
            'note_id': self.note_id,
            'term': self.term,
            'definition': self.definition,
            'importance': self.importance,
            'mastery_level': self.mastery_level,
            'times_reviewed': self.times_reviewed,
            'last_reviewed': self.last_reviewed.isoformat() if self.last_reviewed else None,
            'created_at': self.created_at.isoformat()
        }

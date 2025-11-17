"""
Database Models for Hybrid Voice Chatbot
Contains all SQLAlchemy ORM models
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database import db


class User(db.Model):
    """User model for authentication and tracking"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('user', 'admin', name='user_roles'), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    knowledge_created = db.relationship('KnowledgeBase', foreign_keys='KnowledgeBase.created_by', backref='creator', lazy='dynamic')
    knowledge_approved = db.relationship('KnowledgeBase', foreign_keys='KnowledgeBase.approved_by', backref='approver', lazy='dynamic')
    sessions = db.relationship('Session', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    analytics = db.relationship('Analytics', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class Conversation(db.Model):
    """Conversation model for storing chat history"""
    __tablename__ = 'conversations'
    
    conversation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.Enum('text', 'voice', name='message_types'), default='text')
    sentiment = db.Column(db.Enum('positive', 'negative', 'neutral', name='sentiment_types'), default='neutral')
    confidence_score = db.Column(db.Float, default=0.0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    session_id = db.Column(db.String(100), db.ForeignKey('sessions.session_id'))
    
    # Relationships
    feedback = db.relationship('Feedback', backref='conversation', uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'conversation_id': self.conversation_id,
            'user_id': self.user_id,
            'message': self.message,
            'response': self.response,
            'message_type': self.message_type,
            'sentiment': self.sentiment,
            'confidence_score': self.confidence_score,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'session_id': self.session_id
        }
    
    def __repr__(self):
        return f'<Conversation {self.conversation_id}>'


class Feedback(db.Model):
    """Feedback model for user ratings"""
    __tablename__ = 'feedback'
    
    feedback_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.conversation_id'), nullable=False, unique=True)
    rating = db.Column(db.Enum('good', 'bad', 'improvement', name='rating_types'), nullable=False)
    comments = db.Column(db.Text)
    helpful = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'feedback_id': self.feedback_id,
            'conversation_id': self.conversation_id,
            'rating': self.rating,
            'comments': self.comments,
            'helpful': self.helpful,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Feedback {self.feedback_id} - {self.rating}>'


class KnowledgeBase(db.Model):
    """Knowledge base model for learning system"""
    __tablename__ = 'knowledge_base'
    
    kb_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), default='general')
    approved_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='kb_status'), default='pending', index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    confidence_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    usage_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'kb_id': self.kb_id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'status': self.status,
            'confidence_score': self.confidence_score,
            'created_by': self.created_by,
            'approved_by': self.approved_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'usage_count': self.usage_count
        }
    
    def __repr__(self):
        return f'<KnowledgeBase {self.kb_id} - {self.status}>'


class Session(db.Model):
    """Session model for tracking user sessions"""
    __tablename__ = 'sessions'
    
    session_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    
    # Relationships
    conversations = db.relationship('Conversation', backref='session', lazy='dynamic')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'ip_address': self.ip_address,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }
    
    def __repr__(self):
        return f'<Session {self.session_id}>'


class Analytics(db.Model):
    """Analytics model for user statistics"""
    __tablename__ = 'analytics'
    
    analytics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    total_questions = db.Column(db.Integer, default=0)
    positive_feedback = db.Column(db.Integer, default=0)
    negative_feedback = db.Column(db.Integer, default=0)
    avg_response_time = db.Column(db.Float, default=0.0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'analytics_id': self.analytics_id,
            'user_id': self.user_id,
            'total_questions': self.total_questions,
            'positive_feedback': self.positive_feedback,
            'negative_feedback': self.negative_feedback,
            'avg_response_time': self.avg_response_time,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Analytics User:{self.user_id}>'

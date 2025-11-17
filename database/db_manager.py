"""
Database Manager for Hybrid Voice Chatbot
Handles all database operations
"""
from datetime import datetime
from sqlalchemy import func, desc
from database import db
from database.models import User, Conversation, Feedback, KnowledgeBase, Session, Analytics


class DatabaseManager:
    """Manages all database operations"""
    
    def __init__(self, db_instance):
        self.db = db_instance
    
    # ==================== User Operations ====================
    
    def create_user(self, username, email, password, role='user'):
        """Create a new user"""
        user = User(username=username, email=email, role=role)
        user.set_password(password)
        
        self.db.session.add(user)
        self.db.session.commit()
        
        # Create analytics entry
        analytics = Analytics(user_id=user.user_id)
        self.db.session.add(analytics)
        self.db.session.commit()
        
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        return User.query.get(user_id)
    
    def get_user_by_username(self, username):
        """Get user by username"""
        return User.query.filter_by(username=username).first()
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return User.query.filter_by(email=email).first()
    
    def get_all_users(self, page=1, per_page=20):
        """Get all users with pagination"""
        return User.query.paginate(page=page, per_page=per_page, error_out=False)
    
    def update_user(self, user_id, **kwargs):
        """Update user information"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'password_hash':
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        self.db.session.commit()
        return user
    
    def delete_user(self, user_id):
        """Delete a user"""
        user = self.get_user_by_id(user_id)
        if user:
            self.db.session.delete(user)
            self.db.session.commit()
            return True
        return False
    
    # ==================== Conversation Operations ====================
    
    def create_conversation(self, user_id, message, response, message_type='text', 
                          sentiment='neutral', confidence_score=0.0, session_id=None):
        """Create a new conversation record"""
        conversation = Conversation(
            user_id=user_id,
            message=message,
            response=response,
            message_type=message_type,
            sentiment=sentiment,
            confidence_score=confidence_score,
            session_id=session_id
        )
        
        self.db.session.add(conversation)
        self.db.session.commit()
        
        # Update analytics
        self.update_analytics(user_id, new_question=True)
        
        return conversation
    
    def get_conversation_by_id(self, conversation_id):
        """Get conversation by ID"""
        return Conversation.query.get(conversation_id)
    
    def get_user_conversations(self, user_id, page=1, per_page=20):
        """Get all conversations for a user"""
        return Conversation.query.filter_by(user_id=user_id)\
            .order_by(desc(Conversation.timestamp))\
            .paginate(page=page, per_page=per_page, error_out=False)
    
    def get_recent_conversations(self, limit=10):
        """Get recent conversations across all users"""
        return Conversation.query.order_by(desc(Conversation.timestamp)).limit(limit).all()
    
    def search_conversations(self, query, user_id=None):
        """Search conversations by message content"""
        search = f"%{query}%"
        q = Conversation.query.filter(
            db.or_(
                Conversation.message.like(search),
                Conversation.response.like(search)
            )
        )
        
        if user_id:
            q = q.filter_by(user_id=user_id)
        
        return q.order_by(desc(Conversation.timestamp)).all()
    
    # ==================== Feedback Operations ====================
    
    def create_feedback(self, conversation_id, rating, comments=None, helpful=True):
        """Create feedback for a conversation"""
        feedback = Feedback(
            conversation_id=conversation_id,
            rating=rating,
            comments=comments,
            helpful=helpful
        )
        
        self.db.session.add(feedback)
        self.db.session.commit()
        
        # Update analytics based on rating
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            if rating == 'good':
                self.update_analytics(conversation.user_id, positive_feedback=True)
            elif rating == 'bad':
                self.update_analytics(conversation.user_id, negative_feedback=True)
        
        return feedback
    
    def get_feedback_by_id(self, feedback_id):
        """Get feedback by ID"""
        return Feedback.query.get(feedback_id)
    
    def get_all_feedback(self, page=1, per_page=20):
        """Get all feedback with pagination"""
        return Feedback.query.order_by(desc(Feedback.created_at))\
            .paginate(page=page, per_page=per_page, error_out=False)
    
    def get_feedback_stats(self):
        """Get feedback statistics"""
        total = Feedback.query.count()
        good = Feedback.query.filter_by(rating='good').count()
        bad = Feedback.query.filter_by(rating='bad').count()
        improvement = Feedback.query.filter_by(rating='improvement').count()
        
        return {
            'total': total,
            'good': good,
            'bad': bad,
            'improvement': improvement,
            'good_percentage': (good / total * 100) if total > 0 else 0,
            'bad_percentage': (bad / total * 100) if total > 0 else 0
        }
    
    # ==================== Knowledge Base Operations ====================
    
    def create_knowledge(self, question, answer, created_by, category='general', 
                        status='pending', confidence_score=0.0):
        """Create a knowledge base entry"""
        kb = KnowledgeBase(
            question=question,
            answer=answer,
            created_by=created_by,
            category=category,
            status=status,
            confidence_score=confidence_score
        )
        
        self.db.session.add(kb)
        self.db.session.commit()
        return kb
    
    def get_knowledge_by_id(self, kb_id):
        """Get knowledge base entry by ID"""
        return KnowledgeBase.query.get(kb_id)
    
    def get_all_knowledge(self, status=None, page=1, per_page=20):
        """Get all knowledge base entries"""
        query = KnowledgeBase.query
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(desc(KnowledgeBase.created_at))\
            .paginate(page=page, per_page=per_page, error_out=False)
    
    def get_approved_knowledge(self):
        """Get all approved knowledge"""
        return KnowledgeBase.query.filter_by(status='approved').all()
    
    def get_pending_knowledge(self):
        """Get all pending knowledge"""
        return KnowledgeBase.query.filter_by(status='pending')\
            .order_by(desc(KnowledgeBase.created_at)).all()
    
    def approve_knowledge(self, kb_id, approved_by):
        """Approve a knowledge base entry"""
        kb = self.get_knowledge_by_id(kb_id)
        if kb:
            kb.status = 'approved'
            kb.approved_by = approved_by
            kb.approved_at = datetime.utcnow()
            self.db.session.commit()
            return kb
        return None
    
    def reject_knowledge(self, kb_id):
        """Reject a knowledge base entry"""
        kb = self.get_knowledge_by_id(kb_id)
        if kb:
            kb.status = 'rejected'
            self.db.session.commit()
            return kb
        return None
    
    def increment_knowledge_usage(self, kb_id):
        """Increment usage count for knowledge entry"""
        kb = self.get_knowledge_by_id(kb_id)
        if kb:
            kb.usage_count += 1
            self.db.session.commit()
    
    def search_knowledge(self, query):
        """Search knowledge base"""
        search = f"%{query}%"
        return KnowledgeBase.query.filter(
            db.and_(
                KnowledgeBase.status == 'approved',
                db.or_(
                    KnowledgeBase.question.like(search),
                    KnowledgeBase.answer.like(search)
                )
            )
        ).all()
    
    # ==================== Session Operations ====================
    
    def create_session(self, session_id, user_id=None, ip_address=None, user_agent=None):
        """Create a new session"""
        session = Session(
            session_id=session_id,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.session.add(session)
        self.db.session.commit()
        return session
    
    def get_session(self, session_id):
        """Get session by ID"""
        return Session.query.get(session_id)
    
    def end_session(self, session_id):
        """End a session"""
        session = self.get_session(session_id)
        if session:
            session.ended_at = datetime.utcnow()
            self.db.session.commit()
            return session
        return None
    
    # ==================== Analytics Operations ====================
    
    def get_analytics(self, user_id):
        """Get analytics for a user"""
        return Analytics.query.filter_by(user_id=user_id).first()
    
    def update_analytics(self, user_id, new_question=False, 
                        positive_feedback=False, negative_feedback=False):
        """Update analytics for a user"""
        analytics = self.get_analytics(user_id)
        
        if not analytics:
            analytics = Analytics(user_id=user_id)
            self.db.session.add(analytics)
        
        if new_question:
            analytics.total_questions += 1
        
        if positive_feedback:
            analytics.positive_feedback += 1
        
        if negative_feedback:
            analytics.negative_feedback += 1
        
        analytics.updated_at = datetime.utcnow()
        self.db.session.commit()
        return analytics
    
    def get_global_analytics(self):
        """Get global analytics"""
        total_users = User.query.count()
        total_conversations = Conversation.query.count()
        total_feedback = Feedback.query.count()
        total_knowledge = KnowledgeBase.query.filter_by(status='approved').count()
        pending_knowledge = KnowledgeBase.query.filter_by(status='pending').count()
        
        return {
            'total_users': total_users,
            'total_conversations': total_conversations,
            'total_feedback': total_feedback,
            'total_knowledge': total_knowledge,
            'pending_knowledge': pending_knowledge,
            'feedback_stats': self.get_feedback_stats()
        }

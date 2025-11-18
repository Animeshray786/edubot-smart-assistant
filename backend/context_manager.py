"""
Context Memory Manager
Manages conversation context across sessions with session storage and database persistence
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
from database.db_manager import db

class ConversationContext(db.Model):
    """Database model for storing conversation context"""
    __tablename__ = 'conversation_contexts'
    
    context_id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    context_data = db.Column(db.Text, nullable=False)  # JSON string
    message_count = db.Column(db.Integer, default=0)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'context_id': self.context_id,
            'session_id': self.session_id,
            'user_id': self.user_id,
            'context_data': json.loads(self.context_data) if self.context_data else [],
            'message_count': self.message_count,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class ContextMemoryManager:
    """Manages conversation context and memory"""
    
    def __init__(self, max_context_messages=20, context_window_hours=24):
        """
        Initialize context memory manager
        
        Args:
            max_context_messages: Maximum number of messages to keep in context
            context_window_hours: Hours to keep context active
        """
        self.max_context_messages = max_context_messages
        self.context_window_hours = context_window_hours
        
    def save_context(self, session_id: str, messages: List[Dict], 
                     user_id: Optional[int] = None) -> bool:
        """
        Save conversation context to database
        
        Args:
            session_id: Unique session identifier
            messages: List of message dictionaries
            user_id: Optional user ID for logged-in users
            
        Returns:
            bool: Success status
        """
        try:
            # Limit context to recent messages
            recent_messages = messages[-self.max_context_messages:] if len(messages) > self.max_context_messages else messages
            
            # Find or create context
            context = ConversationContext.query.filter_by(session_id=session_id).first()
            
            if context:
                # Update existing context
                context.context_data = json.dumps(recent_messages)
                context.message_count = len(recent_messages)
                context.last_active = datetime.utcnow()
                context.user_id = user_id
            else:
                # Create new context
                context = ConversationContext(
                    session_id=session_id,
                    user_id=user_id,
                    context_data=json.dumps(recent_messages),
                    message_count=len(recent_messages),
                    last_active=datetime.utcnow()
                )
                db.session.add(context)
            
            db.session.commit()
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to save context: {e}")
            db.session.rollback()
            return False
    
    def load_context(self, session_id: str) -> Optional[Dict]:
        """
        Load conversation context from database
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            dict: Context data or None if not found/expired
        """
        try:
            context = ConversationContext.query.filter_by(session_id=session_id).first()
            
            if not context:
                return None
            
            # Check if context is expired
            expiry_time = datetime.utcnow() - timedelta(hours=self.context_window_hours)
            if context.last_active < expiry_time:
                # Context expired, delete it
                db.session.delete(context)
                db.session.commit()
                return None
            
            # Update last active time
            context.last_active = datetime.utcnow()
            db.session.commit()
            
            return context.to_dict()
            
        except Exception as e:
            print(f"[ERROR] Failed to load context: {e}")
            return None
    
    def get_recent_messages(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Get recent messages from context
        
        Args:
            session_id: Unique session identifier
            limit: Number of recent messages to retrieve
            
        Returns:
            list: Recent messages
        """
        context_data = self.load_context(session_id)
        
        if not context_data:
            return []
        
        messages = context_data.get('context_data', [])
        return messages[-limit:] if len(messages) > limit else messages
    
    def append_message(self, session_id: str, message: Dict, user_id: Optional[int] = None) -> bool:
        """
        Append a new message to context
        
        Args:
            session_id: Unique session identifier
            message: Message dictionary with 'sender' and 'text' keys
            user_id: Optional user ID
            
        Returns:
            bool: Success status
        """
        try:
            context_data = self.load_context(session_id)
            
            # Add timestamp if not present
            if 'timestamp' not in message:
                message['timestamp'] = datetime.utcnow().isoformat()
            
            if context_data:
                messages = context_data.get('context_data', [])
                messages.append(message)
            else:
                messages = [message]
            
            return self.save_context(session_id, messages, user_id)
            
        except Exception as e:
            print(f"[ERROR] Failed to append message: {e}")
            return False
    
    def clear_context(self, session_id: str) -> bool:
        """
        Clear conversation context
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            bool: Success status
        """
        try:
            context = ConversationContext.query.filter_by(session_id=session_id).first()
            
            if context:
                db.session.delete(context)
                db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to clear context: {e}")
            db.session.rollback()
            return False
    
    def get_user_contexts(self, user_id: int, limit: int = 10) -> List[Dict]:
        """
        Get all contexts for a user
        
        Args:
            user_id: User ID
            limit: Maximum number of contexts to retrieve
            
        Returns:
            list: List of context dictionaries
        """
        try:
            contexts = ConversationContext.query.filter_by(user_id=user_id)\
                .order_by(ConversationContext.last_active.desc())\
                .limit(limit)\
                .all()
            
            return [ctx.to_dict() for ctx in contexts]
            
        except Exception as e:
            print(f"[ERROR] Failed to get user contexts: {e}")
            return []
    
    def cleanup_old_contexts(self, days_old: int = 7) -> int:
        """
        Clean up contexts older than specified days
        
        Args:
            days_old: Number of days to keep contexts
            
        Returns:
            int: Number of contexts deleted
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            old_contexts = ConversationContext.query.filter(
                ConversationContext.last_active < cutoff_date
            ).all()
            
            count = len(old_contexts)
            
            for context in old_contexts:
                db.session.delete(context)
            
            db.session.commit()
            
            print(f"[OK] Cleaned up {count} old contexts")
            return count
            
        except Exception as e:
            print(f"[ERROR] Failed to cleanup contexts: {e}")
            db.session.rollback()
            return 0
    
    def get_context_summary(self, session_id: str) -> Dict:
        """
        Get summary of conversation context
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            dict: Context summary with stats
        """
        context_data = self.load_context(session_id)
        
        if not context_data:
            return {
                'exists': False,
                'message_count': 0,
                'user_messages': 0,
                'bot_messages': 0
            }
        
        messages = context_data.get('context_data', [])
        user_messages = len([m for m in messages if m.get('sender') == 'user'])
        bot_messages = len([m for m in messages if m.get('sender') == 'bot'])
        
        return {
            'exists': True,
            'message_count': len(messages),
            'user_messages': user_messages,
            'bot_messages': bot_messages,
            'last_active': context_data.get('last_active'),
            'created_at': context_data.get('created_at')
        }
    
    def extract_context_keywords(self, session_id: str, top_n: int = 10) -> List[str]:
        """
        Extract top keywords from conversation context
        
        Args:
            session_id: Unique session identifier
            top_n: Number of top keywords to return
            
        Returns:
            list: Top keywords
        """
        context_data = self.load_context(session_id)
        
        if not context_data:
            return []
        
        messages = context_data.get('context_data', [])
        
        # Simple keyword extraction (can be enhanced with NLP)
        word_freq = {}
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were', 'be',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                      'should', 'may', 'might', 'can', 'what', 'when', 'where', 'who', 'how'}
        
        for message in messages:
            text = message.get('text', '').lower()
            words = text.split()
            
            for word in words:
                # Clean word
                word = word.strip('.,!?;:()[]{}"\'-')
                
                # Skip short words and stop words
                if len(word) < 3 or word in stop_words:
                    continue
                
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, _ in sorted_words[:top_n]]


# Global instance
context_manager = ContextMemoryManager()


def init_context_manager(app):
    """Initialize context memory manager with Flask app"""
    with app.app_context():
        try:
            # Create table if not exists
            db.create_all()
            print(f"[OK] Context Memory Manager initialized")
            return context_manager
        except Exception as e:
            print(f"[ERROR] Failed to initialize Context Manager: {e}")
            return None

"""
Learning Module for Hybrid Voice Chatbot
Handles NLP processing and self-learning capabilities
"""
from textblob import TextBlob
import re
from datetime import datetime


class LearningModule:
    """Handles learning and NLP operations"""
    
    def __init__(self, db_manager, aiml_engine):
        self.db_manager = db_manager
        self.aiml_engine = aiml_engine
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive', polarity
            elif polarity < -0.1:
                return 'negative', polarity
            else:
                return 'neutral', polarity
                
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return 'neutral', 0.0
    
    def extract_keywords(self, text):
        """Extract keywords from text"""
        try:
            blob = TextBlob(text)
            # Get noun phrases
            keywords = list(blob.noun_phrases)
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {str(e)}")
            return []
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        try:
            # Simple word overlap similarity
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            if len(union) == 0:
                return 0.0
            
            similarity = len(intersection) / len(union)
            return similarity
            
        except Exception as e:
            print(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def find_similar_knowledge(self, question, threshold=0.5):
        """Find similar questions in knowledge base"""
        try:
            approved_knowledge = self.db_manager.get_approved_knowledge()
            
            similar_items = []
            for kb in approved_knowledge:
                similarity = self.calculate_similarity(question, kb.question)
                if similarity >= threshold:
                    similar_items.append({
                        'kb_id': kb.kb_id,
                        'question': kb.question,
                        'answer': kb.answer,
                        'similarity': similarity
                    })
            
            # Sort by similarity
            similar_items.sort(key=lambda x: x['similarity'], reverse=True)
            return similar_items
            
        except Exception as e:
            print(f"Error finding similar knowledge: {str(e)}")
            return []
    
    def process_user_feedback(self, conversation_id, user_answer, user_id):
        """Process user-provided answer for learning"""
        try:
            # Get the conversation
            conversation = self.db_manager.get_conversation_by_id(conversation_id)
            if not conversation:
                return None
            
            # Check if similar knowledge already exists
            similar = self.find_similar_knowledge(conversation.message)
            
            if similar and similar[0]['similarity'] > 0.8:
                print(f"Similar knowledge already exists: {similar[0]['kb_id']}")
                return None
            
            # Calculate confidence score
            confidence = self._calculate_confidence(user_answer)
            
            # Create new knowledge base entry (pending approval)
            kb = self.db_manager.create_knowledge(
                question=conversation.message,
                answer=user_answer,
                created_by=user_id,
                category='user_submitted',
                status='pending',
                confidence_score=confidence
            )
            
            print(f"✓ Created pending knowledge entry: {kb.kb_id}")
            return kb
            
        except Exception as e:
            print(f"Error processing user feedback: {str(e)}")
            return None
    
    def _calculate_confidence(self, answer):
        """Calculate confidence score for an answer"""
        try:
            # Simple confidence calculation based on answer quality
            score = 0.5  # Base score
            
            # Length check
            word_count = len(answer.split())
            if word_count >= 5:
                score += 0.2
            
            # Sentiment check (prefer neutral to positive answers)
            sentiment, polarity = self.analyze_sentiment(answer)
            if sentiment in ['neutral', 'positive']:
                score += 0.1
            
            # Grammar check
            blob = TextBlob(answer)
            if blob.correct() == answer:
                score += 0.1
            
            # Cap at 1.0
            return min(score, 1.0)
            
        except Exception as e:
            print(f"Error calculating confidence: {str(e)}")
            return 0.5
    
    def auto_approve_high_confidence(self, kb_id, admin_id, threshold=0.95):
        """Auto-approve knowledge with high confidence"""
        try:
            kb = self.db_manager.get_knowledge_by_id(kb_id)
            if not kb:
                return False
            
            if kb.confidence_score >= threshold:
                # Auto-approve
                self.db_manager.approve_knowledge(kb_id, admin_id)
                
                # Add to AIML
                self.add_to_aiml(kb.question, kb.answer)
                
                print(f"✓ Auto-approved high-confidence knowledge: {kb_id}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error auto-approving knowledge: {str(e)}")
            return False
    
    def add_to_aiml(self, question, answer):
        """Add approved knowledge to AIML patterns"""
        try:
            # Clean question for pattern
            pattern = self._clean_pattern(question)
            
            # Add to AIML engine
            success = self.aiml_engine.add_pattern(pattern, answer)
            
            if success:
                print(f"✓ Added to AIML: {pattern}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error adding to AIML: {str(e)}")
            return False
    
    def _clean_pattern(self, text):
        """Clean text for AIML pattern"""
        # Remove special characters
        pattern = re.sub(r'[^\w\s\*]', '', text)
        # Convert to uppercase (AIML standard)
        pattern = pattern.upper()
        # Normalize whitespace
        pattern = ' '.join(pattern.split())
        return pattern
    
    def get_learning_suggestions(self, limit=10):
        """Get suggestions for admin to review"""
        try:
            # Get pending knowledge sorted by confidence
            pending = self.db_manager.get_pending_knowledge()
            
            suggestions = []
            for kb in pending[:limit]:
                suggestions.append({
                    'kb_id': kb.kb_id,
                    'question': kb.question,
                    'answer': kb.answer,
                    'confidence': kb.confidence_score,
                    'created_at': kb.created_at.isoformat() if kb.created_at else None,
                    'recommendation': self._get_recommendation(kb.confidence_score)
                })
            
            return suggestions
            
        except Exception as e:
            print(f"Error getting learning suggestions: {str(e)}")
            return []
    
    def _get_recommendation(self, confidence):
        """Get recommendation based on confidence score"""
        if confidence >= 0.9:
            return 'Highly recommended - Auto-approve'
        elif confidence >= 0.7:
            return 'Recommended - Review and approve'
        elif confidence >= 0.5:
            return 'Moderate - Needs review'
        else:
            return 'Low confidence - Verify carefully'
    
    def bulk_approve_knowledge(self, kb_ids, admin_id):
        """Bulk approve multiple knowledge entries"""
        approved_count = 0
        
        for kb_id in kb_ids:
            try:
                kb = self.db_manager.approve_knowledge(kb_id, admin_id)
                if kb:
                    self.add_to_aiml(kb.question, kb.answer)
                    approved_count += 1
            except Exception as e:
                print(f"Error approving {kb_id}: {str(e)}")
        
        return approved_count
    
    def get_learning_stats(self):
        """Get learning module statistics"""
        try:
            total_knowledge = len(self.db_manager.get_all_knowledge(page=1, per_page=9999).items)
            approved = len(self.db_manager.get_approved_knowledge())
            pending = len(self.db_manager.get_pending_knowledge())
            
            aiml_patterns = self.aiml_engine.get_pattern_count()
            
            return {
                'total_knowledge': total_knowledge,
                'approved': approved,
                'pending': pending,
                'rejected': total_knowledge - approved - pending,
                'aiml_patterns': aiml_patterns,
                'approval_rate': (approved / total_knowledge * 100) if total_knowledge > 0 else 0
            }
            
        except Exception as e:
            print(f"Error getting learning stats: {str(e)}")
            return {}

"""
Conversation Manager - Smart Context Tracking & Natural Dialogue
Handles multi-turn conversations with memory and follow-up questions
"""
from datetime import datetime
import json
from typing import Dict, List, Optional


class ConversationManager:
    """Manages conversation flow with context tracking and smart responses"""
    
    def __init__(self):
        self.conversations = {}  # user_id -> conversation data
        self.topics = {
            'nalanda_info': self.handle_nalanda_conversation,
            'admissions': self.handle_admissions_conversation,
            'placements': self.handle_placements_conversation,
            'courses': self.handle_courses_conversation,
            'campus_life': self.handle_campus_conversation,
        }
        
    def start_conversation(self, user_id: str, topic: str, initial_query: str):
        """Start a new conversation flow"""
        if user_id not in self.conversations:
            self.conversations[user_id] = {
                'history': [],
                'context': {},
                'current_topic': None,
                'step': 0,
                'started_at': datetime.now().isoformat(),
                'satisfaction_rating': None
            }
        
        conversation = self.conversations[user_id]
        conversation['current_topic'] = topic
        conversation['step'] = 1
        conversation['history'].append({
            'role': 'user',
            'message': initial_query,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get appropriate handler
        handler = self.topics.get(topic)
        if handler:
            response = handler(user_id, conversation['step'], initial_query)
        else:
            response = self.handle_general_conversation(user_id, initial_query)
        
        conversation['history'].append({
            'role': 'bot',
            'message': response['text'],
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def continue_conversation(self, user_id: str, user_message: str):
        """Continue existing conversation with context awareness"""
        if user_id not in self.conversations:
            return self.start_conversation(user_id, 'general', user_message)
        
        conversation = self.conversations[user_id]
        conversation['step'] += 1
        conversation['history'].append({
            'role': 'user',
            'message': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        topic = conversation['current_topic']
        handler = self.topics.get(topic, self.handle_general_conversation)
        
        response = handler(user_id, conversation['step'], user_message)
        
        conversation['history'].append({
            'role': 'bot',
            'message': response['text'],
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def handle_nalanda_conversation(self, user_id: str, step: int, message: str) -> Dict:
        """Handle Nalanda college information conversation"""
        conversation = self.conversations[user_id]
        
        if step == 1:
            # Initial response with comprehensive info (already in AIML)
            return {
                'text': 'Showing Nalanda Institute details...',
                'follow_up_questions': [
                    'Tell me about admission process',
                    'What are the placement statistics?',
                    'Show me campus facilities',
                    'What courses are offered?'
                ],
                'requires_feedback': False
            }
        
        elif step == 2:
            # User asked follow-up
            if 'admission' in message.lower():
                conversation['context']['interested_in'] = 'admissions'
                return {
                    'text': 'I see you\'re interested in admissions! Let me provide detailed information...',
                    'follow_up_questions': [
                        'What are the eligibility criteria?',
                        'How to apply online?',
                        'What is the fee structure?',
                        'When do admissions open?'
                    ],
                    'requires_feedback': False
                }
            elif 'placement' in message.lower():
                conversation['context']['interested_in'] = 'placements'
                return {
                    'text': 'Great question about placements! Here are the details...',
                    'follow_up_questions': [
                        'Which companies visit for placements?',
                        'What is the average package?',
                        'How to prepare for placements?',
                        'Any internship opportunities?'
                    ],
                    'requires_feedback': False
                }
            elif 'course' in message.lower() or 'program' in message.lower():
                return {
                    'text': 'Let me show you all available programs...',
                    'follow_up_questions': [
                        'Tell me about B.Tech CSE',
                        'What specializations are available?',
                        'What is the course fee?',
                        'What about M.Tech programs?'
                    ],
                    'requires_feedback': False
                }
            else:
                return {
                    'text': 'I can help you with more specific information!',
                    'follow_up_questions': [
                        'Admission process',
                        'Placement details',
                        'Course information',
                        'Campus facilities'
                    ],
                    'requires_feedback': False
                }
        
        elif step >= 3:
            # After 3+ exchanges, ask for satisfaction
            return {
                'text': self.generate_contextual_response(user_id, message),
                'follow_up_questions': [],
                'requires_feedback': True
            }
    
    def handle_admissions_conversation(self, user_id: str, step: int, message: str) -> Dict:
        """Handle admissions conversation flow"""
        if step == 1:
            return {
                'text': 'I\'ll help you with the admission process for Nalanda Institute!',
                'follow_up_questions': [
                    'What are the eligibility requirements?',
                    'How to apply online?',
                    'What documents are needed?',
                    'What is the selection process?'
                ],
                'requires_feedback': False
            }
        elif step == 2:
            if 'eligibility' in message.lower():
                return {
                    'text': 'Here are the eligibility criteria for different programs...',
                    'follow_up_questions': [
                        'B.Tech eligibility details',
                        'M.Tech eligibility details',
                        'MBA eligibility details',
                        'What entrance exams are accepted?'
                    ],
                    'requires_feedback': False
                }
            elif 'apply' in message.lower():
                return {
                    'text': 'Here\'s the step-by-step application process...',
                    'follow_up_questions': [
                        'How to create an account?',
                        'What is the application fee?',
                        'Important dates?',
                        'Need help with form?'
                    ],
                    'requires_feedback': False
                }
        
        return {
            'text': self.generate_contextual_response(user_id, message),
            'follow_up_questions': [],
            'requires_feedback': step >= 3
        }
    
    def handle_placements_conversation(self, user_id: str, step: int, message: str) -> Dict:
        """Handle placement conversation flow"""
        if step == 1:
            return {
                'text': 'Let me share comprehensive placement information!',
                'follow_up_questions': [
                    'Show placement statistics',
                    'Which companies recruit?',
                    'What is average package?',
                    'How to prepare?'
                ],
                'requires_feedback': False
            }
        
        return {
            'text': self.generate_contextual_response(user_id, message),
            'follow_up_questions': [],
            'requires_feedback': step >= 3
        }
    
    def handle_courses_conversation(self, user_id: str, step: int, message: str) -> Dict:
        """Handle courses conversation flow"""
        if step == 1:
            return {
                'text': 'I\'ll show you all available programs at Nalanda!',
                'follow_up_questions': [
                    'B.Tech programs',
                    'M.Tech programs',
                    'MBA programs',
                    'Ph.D programs'
                ],
                'requires_feedback': False
            }
        
        return {
            'text': self.generate_contextual_response(user_id, message),
            'follow_up_questions': [],
            'requires_feedback': step >= 3
        }
    
    def handle_campus_conversation(self, user_id: str, step: int, message: str) -> Dict:
        """Handle campus life conversation flow"""
        if step == 1:
            return {
                'text': 'Let me tell you about life at Nalanda campus!',
                'follow_up_questions': [
                    'Hostel facilities',
                    'Library and labs',
                    'Sports and recreation',
                    'Food and canteen'
                ],
                'requires_feedback': False
            }
        
        return {
            'text': self.generate_contextual_response(user_id, message),
            'follow_up_questions': [],
            'requires_feedback': step >= 3
        }
    
    def handle_general_conversation(self, user_id: str, message: str) -> Dict:
        """Handle general conversation"""
        return {
            'text': 'I\'m here to help! What would you like to know?',
            'follow_up_questions': [
                'About Nalanda College',
                'Admission process',
                'Placement details',
                'Campus facilities'
            ],
            'requires_feedback': False
        }
    
    def generate_contextual_response(self, user_id: str, message: str) -> str:
        """Generate response based on conversation context"""
        conversation = self.conversations[user_id]
        context = conversation.get('context', {})
        
        # Analyze conversation history for context
        interested_in = context.get('interested_in', 'general')
        
        return f"Based on our conversation about {interested_in}, here's more information..."
    
    def collect_feedback(self, user_id: str, rating: int, comment: str = ''):
        """Collect user satisfaction feedback"""
        if user_id in self.conversations:
            self.conversations[user_id]['satisfaction_rating'] = rating
            self.conversations[user_id]['feedback_comment'] = comment
            self.conversations[user_id]['feedback_time'] = datetime.now().isoformat()
            
            return {
                'success': True,
                'message': 'Thank you for your feedback! It helps us improve.'
            }
        
        return {'success': False, 'message': 'No active conversation found'}
    
    def get_feedback_request(self) -> Dict:
        """Generate feedback request message"""
        return {
            'text': '''
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
    <h2 style="margin: 0 0 15px 0;">💬 How was my response?</h2>
    <p style="margin: 0 0 20px 0; font-size: 16px; opacity: 0.95;">Your feedback helps me serve you better!</p>
    
    <div style="display: flex; justify-content: center; gap: 10px; margin-bottom: 20px;">
        <button onclick="submitFeedback(5)" style="background: white; color: #667eea; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-size: 24px; transition: transform 0.2s;">⭐⭐⭐⭐⭐</button>
        <button onclick="submitFeedback(4)" style="background: white; color: #667eea; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-size: 24px; transition: transform 0.2s;">⭐⭐⭐⭐</button>
        <button onclick="submitFeedback(3)" style="background: white; color: #667eea; border: none; padding: 12px 20px; border-radius: 8px; cursor: pointer; font-size: 24px; transition: transform 0.2s;">⭐⭐⭐</button>
    </div>
    
    <p style="margin: 0; font-size: 14px; opacity: 0.85;">Click to rate (5 = Excellent, 3 = Good)</p>
</div>
            ''',
            'is_feedback_request': True
        }
    
    def get_conversation_summary(self, user_id: str) -> Optional[Dict]:
        """Get conversation summary for a user"""
        if user_id not in self.conversations:
            return None
        
        conversation = self.conversations[user_id]
        return {
            'topic': conversation.get('current_topic'),
            'message_count': len(conversation.get('history', [])),
            'duration': conversation.get('started_at'),
            'satisfaction_rating': conversation.get('satisfaction_rating'),
            'context': conversation.get('context', {})
        }


# Global instance
conversation_manager = ConversationManager()

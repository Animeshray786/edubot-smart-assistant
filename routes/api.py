"""
API Routes for Hybrid Voice Chatbot
Main REST API endpoints
"""
from flask import Blueprint, request, session, jsonify, current_app
from database import db
from database.db_manager import DatabaseManager
from backend.utils import login_required, success_response, error_response
from backend.smart_features import smart_features
from backend.extended_features import extended_features
from backend.advanced_features_part2 import advanced_features
from backend.mega_features import mega_features
from backend.ai_features import ai_features
from backend.student_tools import student_tools
from backend.intelligent_response_system import IntelligentResponseSystem
from backend.text_formatter import TextFormatter
from backend.html_formatter import HTMLFormatter
from datetime import datetime
import re

api_bp = Blueprint('api', __name__)
db_manager = DatabaseManager(db)


@api_bp.route('/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return error_response('Message required', 400)
        
        # Get user_id from session or use guest
        user_id = session.get('user_id', 0)  # 0 for guest users
        
        # Get AIML engine from app
        aiml_engine = current_app.aiml_engine
        
        # Initialize Intelligent Response System
        intelligent_system = IntelligentResponseSystem()
        
        # Check for smart features first
        smart_response = handle_smart_features(message)
        if smart_response:
            response = smart_response
            quick_actions = []
            category = 'smart_feature'
        else:
            # Try Intelligent Response System for deep analysis
            analysis_result = intelligent_system.analyze_and_respond(message, {
                'user_id': user_id,
                'session_id': session.get('session_id', 'default')
            })
            
            if analysis_result:
                response = analysis_result
                # Only add generic quick actions for specific intent types
                quick_actions = []
                category = 'intelligent'
            else:
                # Try Student Helpdesk for educational queries
                from backend.student_helpdesk import StudentHelpdeskBot
                helpdesk = StudentHelpdeskBot()
                helpdesk_response = helpdesk.process_query(message, user_id)
                
                # If helpdesk handled it, use that response
                if helpdesk_response and 'response' in helpdesk_response:
                    response = helpdesk_response['response']
                    quick_actions = helpdesk_response.get('quick_actions', [])
                    category = helpdesk_response.get('category', 'general')
                else:
                    # Fall back to AIML engine
                    response = aiml_engine.get_response(message, session.get('session_id', 'default'))
                    quick_actions = []
                    category = 'general'
        
        # Analyze sentiment
        from backend.learning_module import LearningModule
        learning = LearningModule(db_manager, aiml_engine)
        sentiment, confidence = learning.analyze_sentiment(message)
        
        # Track knowledge gaps for failed queries
        is_successful = True
        if response and any(phrase in response.lower() for phrase in [
            "i don't understand", "i'm not sure", "could you rephrase", 
            "i don't know", "sorry, i couldn't", "no information"
        ]):
            is_successful = False
            # Track in knowledge gap analyzer
            try:
                knowledge_gap = current_app.knowledge_gap
                knowledge_gap.analyze_failed_query(
                    query=message,
                    user_id=user_id,
                    sentiment=sentiment,
                    confidence=confidence
                )
            except Exception as e:
                print(f"Knowledge gap tracking error: {e}")
        
        # Save conversation only if user is logged in
        if user_id > 0:
            conversation = db_manager.create_conversation(
                user_id=user_id,
                message=message,
                response=response,
                message_type='text',
                sentiment=sentiment,
                confidence_score=confidence,
                session_id=session.get('session_id')
            )
            conversation_id = conversation.conversation_id
        else:
            conversation_id = 0  # Guest conversation
        
        return success_response({
            'conversation_id': conversation_id,
            'message': message,
            'response': response,
            'sentiment': sentiment,
            'category': category,
            'quick_actions': quick_actions,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return error_response('Chat failed', 500)


@api_bp.route('/voice-input', methods=['POST'])
@login_required
def voice_input():
    """Process voice input"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return error_response('Voice message required', 400)
        
        # Get response from AIML engine
        aiml_engine = current_app.aiml_engine
        response = aiml_engine.get_response(message, session.get('session_id', 'default'))
        
        # Analyze sentiment
        from backend.learning_module import LearningModule
        learning = LearningModule(db_manager, aiml_engine)
        sentiment, confidence = learning.analyze_sentiment(message)
        
        # Save conversation
        conversation = db_manager.create_conversation(
            user_id=session['user_id'],
            message=message,
            response=response,
            message_type='voice',
            sentiment=sentiment,
            confidence_score=confidence,
            session_id=session.get('session_id')
        )
        
        # Generate TTS (optional - can be done client-side)
        tts_enabled = data.get('tts', False)
        audio_file = None
        
        if tts_enabled:
            from backend.voice_processor import VoiceProcessor
            voice = VoiceProcessor()
            audio_file = voice.text_to_speech(response)
        
        return success_response({
            'conversation_id': conversation.conversation_id,
            'message': message,
            'response': response,
            'sentiment': sentiment,
            'audio_file': audio_file,
            'timestamp': conversation.timestamp.isoformat()
        })
        
    except Exception as e:
        print(f"Error in voice input: {str(e)}")
        return error_response('Voice processing failed', 500)


@api_bp.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    """Submit feedback for a conversation"""
    try:
        data = request.get_json()
        
        conversation_id = data.get('conversation_id')
        rating = data.get('rating')
        comments = data.get('comments', '')
        user_answer = data.get('user_answer', '')
        
        if not conversation_id or not rating:
            return error_response('Conversation ID and rating required', 400)
        
        # Collect feedback
        from backend.feedback_collector import FeedbackCollector
        feedback_collector = FeedbackCollector(db_manager)
        feedback, msg = feedback_collector.collect_feedback(
            conversation_id, rating, comments
        )
        
        if not feedback:
            return error_response(msg, 400)
        
        # If user provided answer for learning mode
        if user_answer and rating in ['bad', 'improvement']:
            aiml_engine = current_app.aiml_engine
            from backend.learning_module import LearningModule
            learning = LearningModule(db_manager, aiml_engine)
            kb = learning.process_user_feedback(
                conversation_id, user_answer, session['user_id']
            )
            
            if kb:
                return success_response({
                    'feedback': feedback.to_dict(),
                    'learning_submitted': True,
                    'kb_id': kb.kb_id,
                    'message': 'Feedback submitted and added to learning queue'
                })
        
        return success_response({
            'feedback': feedback.to_dict(),
            'message': 'Feedback submitted successfully'
        })
        
    except Exception as e:
        print(f"Error submitting feedback: {str(e)}")
        return error_response('Feedback submission failed', 500)


@api_bp.route('/chat-history', methods=['GET'])
@login_required
def get_chat_history():
    """Get user's chat history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        conversations = db_manager.get_user_conversations(
            session['user_id'], page, per_page
        )
        
        return success_response({
            'conversations': [c.to_dict() for c in conversations.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': conversations.total,
                'pages': conversations.pages
            }
        })
        
    except Exception as e:
        print(f"Error getting chat history: {str(e)}")
        return error_response('Failed to get chat history', 500)


@api_bp.route('/knowledge', methods=['GET'])
def get_knowledge():
    """Get approved knowledge base entries"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        knowledge = db_manager.get_all_knowledge('approved', page, per_page)
        
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
        print(f"Error getting knowledge: {str(e)}")
        return error_response('Failed to get knowledge', 500)


def handle_smart_features(message):
    """
    Handle smart feature requests (Features 1-30+)
    Returns response if matched, None otherwise
    """
    msg_lower = message.lower()
    
    # === NALANDA COLLEGE QUICK ACTIONS ===
    
    # Admissions Quick Action
    if msg_lower in ['admissions', 'admission']:
        return """
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>🎓 Nalanda Institute Admissions</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #667eea;">📋 Admission Process:</h3>
    <ol style="line-height: 2;">
        <li><strong>Apply Online:</strong> <a href="https://www.thenalanda.com/admissions" target="_blank">thenalanda.com/admissions</a></li>
        <li><strong>Entrance Exam:</strong> JEE Main for B.Tech</li>
        <li><strong>Merit Selection:</strong> Based on exam scores</li>
        <li><strong>Document Verification:</strong> Original certificates</li>
        <li><strong>Fee Payment:</strong> Multiple payment options</li>
    </ol>
    
    <h3 style="color: #667eea; margin-top: 20px;">✅ Eligibility:</h3>
    <ul style="line-height: 2;">
        <li><strong>B.Tech:</strong> 10+2 PCM with 50%+ marks</li>
        <li><strong>M.Tech:</strong> B.Tech/BE with 55%+ marks</li>
    </ul>
    
    <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
        <strong>📞 Contact:</strong> +91 99371 65074<br>
        <strong>📧 Email:</strong> info@thenalanda.com<br>
        <strong>🌐 Website:</strong> <a href="https://www.thenalanda.com" target="_blank">thenalanda.com</a>
    </div>
</div>
"""
    
    # Placements Quick Action
    if msg_lower in ['placements', 'placement', 'jobs']:
        return """
<div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>💼 Nalanda Placement Records</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #11998e;">📊 Placement Statistics 2024:</h3>
    <ul style="line-height: 2;">
        <li>🎯 <strong>Placement Rate:</strong> 85-90%</li>
        <li>💰 <strong>Highest Package:</strong> Rs 45 LPA</li>
        <li>💵 <strong>Average Package:</strong> Rs 6.5 LPA</li>
        <li>🏢 <strong>Companies Visiting:</strong> 150+ annually</li>
    </ul>
    
    <h3 style="color: #11998e; margin-top: 20px;">🌟 Top Recruiters:</h3>
    <p style="line-height: 2;">
        <strong>Tech Giants:</strong> Amazon, Microsoft, Google, Adobe<br>
        <strong>IT Services:</strong> TCS, Infosys, Wipro, Accenture<br>
        <strong>Core Companies:</strong> L&T, Siemens, ABB, BHEL, NTPC<br>
        <strong>Consulting:</strong> Deloitte, E&Y, KPMG, PwC<br>
        <strong>Startups:</strong> Flipkart, Paytm, PhonePe, Swiggy
    </p>
    
    <h3 style="color: #11998e; margin-top: 20px;">🎓 Training & Preparation:</h3>
    <ul style="line-height: 2;">
        <li>✅ Aptitude & reasoning sessions</li>
        <li>✅ Coding & technical training</li>
        <li>✅ Soft skills development</li>
        <li>✅ Mock interviews & GD practice</li>
        <li>✅ Resume building workshops</li>
    </ul>
    
    <div style="margin-top: 20px; padding: 15px; background: #e8f5e9; border-radius: 8px; border-left: 4px solid #4caf50;">
        <strong>📞 Placement Cell:</strong> +91 99371 65074<br>
        <strong>🌐 More Info:</strong> <a href="https://www.thenalanda.com/placement" target="_blank">thenalanda.com/placement</a>
    </div>
</div>
"""
    
    # Smart Study Quick Action
    if msg_lower in ['smart study', 'study smart', 'smart features']:
        return """
<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>🧠 Smart Study Features - AI-Powered Learning</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #f5576c;">🎯 Study Planning & Organization:</h3>
    <ul style="line-height: 2;">
        <li>📅 <strong>Custom Study Plans:</strong> Say "study plan 2025-12-31"</li>
        <li>⏰ <strong>Pomodoro Timer:</strong> Say "pomodoro timer"</li>
        <li>⚡ <strong>Quick Revision:</strong> Say "quick revision Math"</li>
        <li>📊 <strong>Performance Prediction:</strong> Say "predict my performance"</li>
    </ul>
    
    <h3 style="color: #f5576c; margin-top: 20px;">💡 Learning Techniques:</h3>
    <ul style="line-height: 2;">
        <li>🧠 <strong>Memory Techniques:</strong> Say "memory technique"</li>
        <li>📝 <strong>Note-Taking Methods:</strong> Say "how to take notes"</li>
        <li>🗺️ <strong>Mind Mapping:</strong> Say "mind map [topic]"</li>
        <li>📚 <strong>Reading Strategies:</strong> Say "reading technique"</li>
        <li>⚡ <strong>Speed Learning:</strong> Say "speed learning"</li>
    </ul>
    
    <h3 style="color: #f5576c; margin-top: 20px;">🎓 Exam Preparation:</h3>
    <ul style="line-height: 2;">
        <li>✅ <strong>Exam Tips:</strong> Say "exam tips"</li>
        <li>📋 <strong>Exam Pattern Analysis:</strong> Say "exam pattern"</li>
        <li>😰 <strong>Anxiety Management:</strong> Say "exam anxiety"</li>
        <li>📝 <strong>Flashcards:</strong> Say "flashcard [topic]"</li>
    </ul>
    
    <h3 style="color: #f5576c; margin-top: 20px;">💪 Productivity & Wellness:</h3>
    <ul style="line-height: 2;">
        <li>🎯 <strong>Focus Improvement:</strong> Say "concentration"</li>
        <li>😌 <strong>Stress Relief:</strong> Say "I am stressed"</li>
        <li>⚡ <strong>Beat Procrastination:</strong> Say "procrastination"</li>
        <li>💤 <strong>Sleep Optimization:</strong> Say "sleep optimization"</li>
        <li>🍎 <strong>Brain Foods:</strong> Say "brain food"</li>
        <li>🎵 <strong>Study Music:</strong> Say "study music"</li>
    </ul>
    
    <h3 style="color: #f5576c; margin-top: 20px;">🎮 Gamification:</h3>
    <ul style="line-height: 2;">
        <li>🏆 <strong>Focus Challenge:</strong> Say "focus challenge"</li>
        <li>👥 <strong>Study Buddy:</strong> Say "study buddy"</li>
        <li>🔥 <strong>Habit Building:</strong> Say "build habit"</li>
    </ul>
    
    <div style="margin-top: 20px; padding: 15px; background: #fff3e0; border-radius: 8px; border-left: 4px solid #ff9800;">
        <strong>💡 Pro Tip:</strong> Try asking specific questions like "How to prepare for exams in 30 days?" or "Best memory technique for history?"<br>
        <strong>🚀 Quick Start:</strong> Say "motivate me" for instant inspiration!
    </div>
</div>
"""
    
    # Campus Info Quick Action
    if msg_lower in ['campus info', 'campus', 'facilities']:
        return """
<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>🏫 Nalanda Campus & Facilities</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #fa709a;">📚 Academic Facilities:</h3>
    <ul style="line-height: 2;">
        <li>📖 <strong>Modern Library</strong> - Digital & physical resources</li>
        <li>💻 <strong>Computer Labs</strong> - Latest technology</li>
        <li>🔬 <strong>Research Centers</strong> - Innovation hubs</li>
        <li>🎓 <strong>Smart Classrooms</strong> - Interactive learning</li>
        <li>🧪 <strong>Advanced Laboratories</strong> - Hands-on practice</li>
    </ul>
    
    <h3 style="color: #fa709a; margin-top: 20px;">🏠 Accommodation:</h3>
    <ul style="line-height: 2;">
        <li>🛏️ <strong>Separate Hostels</strong> - Boys & Girls</li>
        <li>🔐 <strong>24/7 Security</strong> - Safe environment</li>
        <li>📶 <strong>Wi-Fi Campus</strong> - High-speed internet</li>
        <li>🍽️ <strong>Mess Facilities</strong> - Nutritious meals</li>
        <li>💰 <strong>Hostel Fees:</strong> Rs 40,000-60,000/year</li>
    </ul>
    
    <h3 style="color: #fa709a; margin-top: 20px;">🎯 Student Life:</h3>
    <ul style="line-height: 2;">
        <li>⚽ <strong>Sports Facilities</strong> - Cricket, Football, Badminton</li>
        <li>🍕 <strong>Cafeteria</strong> - Various food options</li>
        <li>🏥 <strong>Medical Center</strong> - 24/7 healthcare</li>
        <li>🎨 <strong>Creativity Hub</strong> - Arts & culture</li>
        <li>🎪 <strong>Multiple Clubs</strong> - Photography, Music, Tech, Sports</li>
    </ul>
    
    <div style="margin-top: 20px; padding: 15px; background: #e1f5fe; border-radius: 8px; border-left: 4px solid #03a9f4;">
        <strong>📍 Location:</strong> Buddhist Villa, Chandaka, Bhubaneswar, Odisha 751024<br>
        <strong>📞 Contact:</strong> +91 99371 65074<br>
        <strong>🌐 More Info:</strong> <a href="https://www.thenalanda.com/facilities" target="_blank">thenalanda.com/facilities</a>
    </div>
</div>
"""
    
    # Fee Structure Quick Action
    if msg_lower in ['fee structure', 'fees', 'fee']:
        return """
<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>💰 Nalanda Fee Structure</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #4facfe;">📋 Academic Fees (Approximate):</h3>
    <ul style="line-height: 2;">
        <li>🎓 <strong>B.Tech:</strong> Rs 80,000 - Rs 1,20,000 per year</li>
        <li>🎓 <strong>M.Tech:</strong> Rs 60,000 - Rs 90,000 per year</li>
        <li>🏠 <strong>Hostel:</strong> Rs 40,000 - Rs 60,000 per year (AC/Non-AC)</li>
        <li>🍽️ <strong>Mess:</strong> Rs 25,000 - Rs 30,000 per year</li>
    </ul>
    
    <h3 style="color: #4facfe; margin-top: 20px;">💳 Payment Options:</h3>
    <ul style="line-height: 2;">
        <li>✅ Online payment portal</li>
        <li>✅ Demand Draft (DD)</li>
        <li>✅ Cash payment at office</li>
        <li>✅ EMI options available</li>
    </ul>
    
    <h3 style="color: #4facfe; margin-top: 20px;">🎁 Scholarships Available:</h3>
    <p style="line-height: 2;">
        Nalanda Institute offers various scholarships for deserving students based on:
        <ul>
            <li>Merit-based performance</li>
            <li>Financial need</li>
            <li>Sports achievements</li>
            <li>Special categories</li>
        </ul>
    </p>
    
    <div style="margin-top: 20px; padding: 15px; background: #fff9c4; border-radius: 8px; border-left: 4px solid #fbc02d;">
        <strong>📞 For Exact Fee Details:</strong> +91 99371 65074<br>
        <strong>📧 Email:</strong> info@thenalanda.com<br>
        <strong>🌐 Fee Portal:</strong> <a href="https://www.thenalanda.com/fees" target="_blank">thenalanda.com/fees</a><br>
        <strong>💡 Note:</strong> Fees are subject to change. Contact for current academic year fees.
    </div>
</div>
"""
    
    # Contact Quick Action
    if msg_lower in ['contact', 'contact info', 'phone']:
        return """
<div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); color: #333; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;">
    <h2>📞 Contact Nalanda Institute</h2>
</div>

<div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <h3 style="color: #667eea;">📱 Primary Contact:</h3>
    <div style="padding: 15px; background: #e8eaf6; border-radius: 8px; margin: 10px 0;">
        <p style="font-size: 18px; margin: 5px 0;"><strong>📞 Phone:</strong> <a href="tel:+919937165074">+91 99371 65074</a></p>
        <p style="font-size: 18px; margin: 5px 0;"><strong>📧 Email:</strong> <a href="mailto:info@thenalanda.com">info@thenalanda.com</a></p>
        <p style="font-size: 18px; margin: 5px 0;"><strong>🌐 Website:</strong> <a href="https://www.thenalanda.com" target="_blank">thenalanda.com</a></p>
    </div>
    
    <h3 style="color: #667eea; margin-top: 20px;">📍 Address:</h3>
    <div style="padding: 15px; background: #e8f5e9; border-radius: 8px; margin: 10px 0;">
        <p style="line-height: 1.8;">
            <strong>Nalanda Institute of Technology</strong><br>
            Buddhist Villa, Chandaka<br>
            Bhubaneswar, Odisha 751024<br>
            India
        </p>
        <p style="margin-top: 10px;">
            <a href="https://www.google.com/maps/dir//Nalanda+Institute+of+Technology" target="_blank" style="color: #4caf50; font-weight: bold;">📍 Get Directions on Google Maps</a>
        </p>
    </div>
    
    <h3 style="color: #667eea; margin-top: 20px;">🌐 Social Media:</h3>
    <div style="padding: 15px; background: #fff3e0; border-radius: 8px; margin: 10px 0;">
        <p style="line-height: 2;">
            📘 <a href="https://www.facebook.com/share/1AG6TvcnQi/" target="_blank">Facebook</a><br>
            📸 <a href="https://www.instagram.com/nalandabbsr" target="_blank">Instagram</a><br>
            🐦 <a href="https://x.com/NALANDABHUBANE1" target="_blank">Twitter/X</a><br>
            💼 <a href="https://www.linkedin.com/company/nalanda-institute-of-technology-bhubaneswar/" target="_blank">LinkedIn</a><br>
            🎥 <a href="https://youtube.com/@nalandabhubaneswar4971" target="_blank">YouTube</a>
        </p>
    </div>
    
    <div style="margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
        <strong>💡 Quick Links:</strong><br>
        • <a href="https://www.thenalanda.com/admissions" target="_blank">Admissions</a><br>
        • <a href="https://www.thenalanda.com/student-portal" target="_blank">Student Portal</a><br>
        • <a href="https://www.thenalanda.com/placement" target="_blank">Placements</a><br>
        • <a href="https://www.thenalanda.com/library" target="_blank">Library</a>
    </div>
</div>
"""
    
    # === FEATURES 11-20: Extended Features ===
    
    # Feature 11: Exam Pattern Analysis
    if 'exam pattern' in msg_lower or 'exam type' in msg_lower or 'mcq strategy' in msg_lower:
        exam_type = 'multiple_choice' if 'mcq' in msg_lower or 'multiple choice' in msg_lower else 'essay' if 'essay' in msg_lower else 'practical' if 'practical' in msg_lower else 'multiple_choice'
        return extended_features.analyze_exam_pattern(exam_type)
    
    # Feature 12: Subject Difficulty Analyzer
    if 'subject difficulty' in msg_lower or 'how hard is' in msg_lower:
        words = msg_lower.split()
        subject = next((word for word in words if word in ['math', 'physics', 'chemistry', 'biology', 'history', 'english']), 'Math')
        level = 'beginner' if 'beginner' in msg_lower else 'intermediate' if 'intermediate' in msg_lower else 'beginner'
        return extended_features.analyze_subject_difficulty(subject, level)
    
    # Feature 13: Smart Flashcard Generator
    if 'flashcard' in msg_lower or 'flash card' in msg_lower:
        topic = message.replace('flashcard', '').replace('flash card', '').replace('create', '').replace('make', '').strip() or 'General Topic'
        return extended_features.generate_flashcards(topic)
    
    # Feature 14: Study Environment Optimizer
    if 'study environment' in msg_lower or 'study space' in msg_lower or 'study setup' in msg_lower:
        return extended_features.optimize_study_environment()
    
    # Feature 15: Mind Map Guide
    if 'mind map' in msg_lower or 'mindmap' in msg_lower or 'concept map' in msg_lower:
        topic = message.replace('mind map', '').replace('mindmap', '').strip() or 'Your Topic'
        return extended_features.generate_mind_map_guide(topic)
    
    # Feature 16: Productivity Hacks
    if 'productivity' in msg_lower and ('hack' in msg_lower or 'tip' in msg_lower):
        return extended_features.get_productivity_hack()
    
    # Feature 17: Exam Day Plan
    if 'exam day' in msg_lower or 'test day' in msg_lower:
        return extended_features.get_exam_day_plan()
    
    # Feature 18: Group Study Guide (Updated to avoid conflict with Feature 9)
    if 'group study' in msg_lower and 'how' in msg_lower:
        return extended_features.get_group_study_guide()
    
    # Feature 19: Reading Technique Guide
    if 'reading technique' in msg_lower or 'sq3r' in msg_lower or 'speed read' in msg_lower:
        technique = 'SQ3R' if 'sq3r' in msg_lower else 'Speed Reading' if 'speed' in msg_lower else None
        return extended_features.get_reading_technique_guide(technique)
    
    # Feature 20: Math Shortcuts
    if 'math shortcut' in msg_lower or 'math trick' in msg_lower or 'mental math' in msg_lower:
        return extended_features.get_math_shortcut_guide()
    
    # === FEATURES 21-27: Advanced Features ===
    
    # Feature 21: Citation Generator
    if any(word in msg_lower for word in ['citation', 'cite', 'reference', 'bibliography']):
        style = 'MLA' if 'mla' in msg_lower else 'Chicago' if 'chicago' in msg_lower else 'APA'
        return advanced_features.generate_citation_guide(style)
    
    # Feature 22: Research Paper Outliner
    if 'research paper' in msg_lower or 'paper outline' in msg_lower:
        paper_type = 'research' if 'research' in msg_lower else 'essay'
        return advanced_features.generate_paper_outline(paper_type, 'Your Topic')
    
    # Feature 23: Concentration Booster
    if 'concentration' in msg_lower or 'focus better' in msg_lower or 'distracted' in msg_lower:
        return advanced_features.concentration_booster_menu()
    
    # Feature 24: Procrastination Destroyer
    if 'procrastinat' in msg_lower or 'lazy' in msg_lower or 'avoiding' in msg_lower:
        return advanced_features.procrastination_destroyer()
    
    # Feature 25: Brain Food Guide
    if 'brain food' in msg_lower or ('what' in msg_lower and 'eat' in msg_lower) or 'study food' in msg_lower:
        return advanced_features.brain_food_guide()
    
    # Feature 26: Sleep Optimization
    if 'sleep' in msg_lower or 'insomnia' in msg_lower or 'tired' in msg_lower:
        return advanced_features.sleep_optimization_guide()
    
    # Feature 27: Study Music Guide
    if 'study music' in msg_lower or 'music for studying' in msg_lower:
        return advanced_features.study_music_guide()
    
    # === FEATURES 28-30: Mega Features ===
    
    # Feature 28: Exam Anxiety Management (more specific than Feature 3)
    if 'exam anxiety' in msg_lower or 'test anxiety' in msg_lower:
        return mega_features.exam_anxiety_destroyer()
    
    # Feature 29: Habit Building
    if 'habit' in msg_lower and ('build' in msg_lower or 'create' in msg_lower or 'track' in msg_lower):
        return mega_features.habit_building_system()
    
    # Feature 30: Speed Learning
    if 'speed learning' in msg_lower or 'learn faster' in msg_lower or 'feynman' in msg_lower:
        return mega_features.speed_learning_system()
    
    # Features 31-60 Summary
    if 'more features' in msg_lower or 'all features' in msg_lower or 'feature list' in msg_lower:
        return mega_features.get_remaining_features_summary()
    
    # === LECTURE NOTE SUMMARIZER ===
    
    # Feature: Lecture Note Summarizer
    if 'summarize' in msg_lower or 'lecture notes' in msg_lower or 'note summary' in msg_lower:
        return """
        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 25px; border-radius: 12px; margin: 15px 0;">
            <h2 style="margin: 0 0 15px 0;"><i class="fas fa-book-reader"></i> Lecture Note Summarizer</h2>
            <p style="font-size: 1.1em; opacity: 0.95; margin-bottom: 20px;">
                Upload your lecture notes or transcripts and get instant AI-powered summaries!
            </p>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; font-size: 1.2em;">✨ What You Get:</h3>
                <ul style="line-height: 2; margin: 0; padding-left: 20px;">
                    <li>Concise bullet-point summaries</li>
                    <li>Key concepts with definitions</li>
                    <li>Auto-generated study questions</li>
                    <li>Compression statistics</li>
                    <li>Beautiful formatted output</li>
                </ul>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 8px; margin-bottom: 15px;">
                <h3 style="margin-top: 0; font-size: 1.2em;">🚀 How to Use:</h3>
                <ol style="line-height: 2; margin: 0; padding-left: 20px;">
                    <li>Go to <strong>Dashboard</strong> → <strong>Lecture Notes</strong></li>
                    <li>Click <strong>"Upload New Note"</strong></li>
                    <li>Paste your lecture content (min 50 words)</li>
                    <li>Add title, subject, and tags</li>
                    <li>Click <strong>"Summarize"</strong> and get instant results!</li>
                </ol>
            </div>
            
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px;">
                <strong>💡 Pro Tip:</strong> The more detailed your notes, the better the summary and study questions!
            </div>
        </div>
        """
    
    # === ORIGINAL FEATURES 1-10 ===
    
    # Feature 1: Study Schedule
    if any(word in msg_lower for word in ['study plan', 'study schedule', 'exam plan']):
        match = re.search(r'\d{4}-\d{2}-\d{2}', message)
        if match:
            return smart_features.calculate_study_schedule(match.group())
        return "📅 Please provide exam date in format: YYYY-MM-DD\nExample: 'study plan 2025-12-15'"
    
    # Feature 2: Pomodoro Timer
    if 'pomodoro' in msg_lower or 'focus timer' in msg_lower:
        match = re.search(r'(\d+)\s*session', msg_lower)
        sessions = int(match.group(1)) if match else 4
        return smart_features.pomodoro_timer(sessions)
    
    # Feature 3: Stress Relief (general, not exam-specific)
    if any(word in msg_lower for word in ['stress', 'anxious', 'nervous', 'worried', 'calm']) and 'exam' not in msg_lower:
        return smart_features.exam_stress_reliever()
    
    # Feature 4: Note Taking
    if 'note' in msg_lower and any(word in msg_lower for word in ['taking', 'making', 'how to']):
        subjects = ['math', 'science', 'history', 'programming', 'languages']
        for subject in subjects:
            if subject in msg_lower:
                return smart_features.smart_note_taking_guide(subject)
        return smart_features.smart_note_taking_guide('general')
    
    # Feature 5: Memory Techniques
    if any(word in msg_lower for word in ['memory', 'remember', 'memorize', 'forget']):
        topic = message.split()[-1] if len(message.split()) > 1 else 'concepts'
        return smart_features.memory_techniques(topic)
    
    # Feature 6: Career Advice
    if any(word in msg_lower for word in ['career', 'job', 'profession', 'future']):
        interests = ['technology', 'business', 'creative', 'science']
        for interest in interests:
            if interest in msg_lower:
                return smart_features.career_path_advisor(interest)
        return smart_features.career_path_advisor('technology')
    
    # Feature 7: Quick Revision
    if 'quick revision' in msg_lower or 'revision sheet' in msg_lower:
        words = message.split()
        subject = words[-1] if len(words) > 2 else 'General'
        topics = words[-2] if len(words) > 3 else 'All topics'
        return smart_features.quick_revision_generator(subject, topics)
    
    # Feature 8: Focus Challenge
    if 'challenge' in msg_lower or 'game' in msg_lower:
        return smart_features.focus_mode_challenge()
    
    # Feature 9: Study Buddy
    if 'study buddy' in msg_lower:
        return smart_features.study_buddy_matcher()
    
    # Feature 10: Performance Predictor
    if 'predict' in msg_lower or 'performance' in msg_lower:
        numbers = re.findall(r'\d+', message)
        if len(numbers) >= 3:
            return smart_features.exam_performance_predictor(
                int(numbers[0]), int(numbers[1]), int(numbers[2])
            )
        return "📊 Format: 'predict performance [current_score] [target_score] [days_left]'\nExample: 'predict performance 60 85 30'"
    
    # Bonus: Random tips
    if any(word in msg_lower for word in ['tip', 'advice', 'help me study']):
        return smart_features.get_study_tip() + "\n\n" + smart_features.get_motivation()
    
    return None


@api_bp.route('/stats', methods=['GET'])
@login_required
def get_user_stats():
    """Get user statistics"""
    try:
        analytics = db_manager.get_analytics(session['user_id'])
        
        if not analytics:
            return success_response({
                'total_questions': 0,
                'positive_feedback': 0,
                'negative_feedback': 0
            })
        
        return success_response(analytics.to_dict())
        
    except Exception as e:
        print(f"Error getting user stats: {str(e)}")
        return error_response('Failed to get stats', 500)


@api_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for conversation satisfaction"""
    try:
        data = request.get_json()
        rating = data.get('rating')
        label = data.get('label', '')
        session_id = data.get('session_id', 'anonymous')
        timestamp = data.get('timestamp', datetime.now().isoformat())
        
        if not rating:
            return error_response('Rating required', 400)
        
        # Store feedback in database
        feedback_data = {
            'user_id': session.get('user_id', 0),
            'session_id': session_id,
            'rating': rating,
            'label': label,
            'timestamp': timestamp,
            'created_at': datetime.now()
        }
        
        # Log feedback
        current_app.logger.info(f"Feedback received: {rating} stars - {label} (Session: {session_id})")
        
        # You can save to database here
        # db_manager.save_feedback(feedback_data)
        
        return success_response({
            'message': 'Feedback received successfully',
            'rating': rating,
            'thank_you': True
        })
        
    except Exception as e:
        print(f"Error submitting feedback: {str(e)}")
        return error_response('Failed to submit feedback', 500)

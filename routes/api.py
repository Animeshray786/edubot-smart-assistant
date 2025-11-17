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
        
        # Check for smart features first
        smart_response = handle_smart_features(message)
        if smart_response:
            response = smart_response
            quick_actions = []
            category = 'smart_feature'
        else:
            # Try Student Helpdesk first for educational queries
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

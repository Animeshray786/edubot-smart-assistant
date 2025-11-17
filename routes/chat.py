"""
Chat Routes for Hybrid Voice Chatbot
Handles main chat interface
"""
from flask import Blueprint, render_template, session, redirect, url_for

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def index():
    """Main EduBot chat interface"""
    return render_template('edubot.html')


@chat_bp.route('/chat')
def chat_page():
    """EduBot chat page"""
    return render_template('edubot.html')


@chat_bp.route('/classic')
def classic_chat():
    """Classic chat interface (fallback)"""
    return render_template('index.html')


@chat_bp.route('/login')
def login_page():
    """Login page"""
    if 'user_id' in session:
        return redirect(url_for('chat.index'))
    return render_template('login.html')


@chat_bp.route('/register')
def register_page():
    """Registration page"""
    if 'user_id' in session:
        return redirect(url_for('chat.index'))
    return render_template('register.html')

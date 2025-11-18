"""
Multi-Language Support (i18n) System
Supports English, Hindi, Spanish, and more languages
"""

from flask_babel import Babel, gettext, lazy_gettext
from flask import session, request
import json
import os

class I18nManager:
    """Internationalization Manager"""
    
    def __init__(self, app=None):
        self.app = app
        self.babel = None
        self.supported_languages = {
            'en': {'name': 'English', 'flag': '🇺🇸'},
            'hi': {'name': 'हिंदी (Hindi)', 'flag': '🇮🇳'},
            'es': {'name': 'Español (Spanish)', 'flag': '🇪🇸'},
            'fr': {'name': 'Français (French)', 'flag': '🇫🇷'},
            'de': {'name': 'Deutsch (German)', 'flag': '🇩🇪'},
            'zh': {'name': '中文 (Chinese)', 'flag': '🇨🇳'},
            'ja': {'name': '日本語 (Japanese)', 'flag': '🇯🇵'},
            'ar': {'name': 'العربية (Arabic)', 'flag': '🇸🇦'},
            'pt': {'name': 'Português (Portuguese)', 'flag': '🇵🇹'},
            'ru': {'name': 'Русский (Russian)', 'flag': '🇷🇺'}
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize i18n with Flask app"""
        self.app = app
        
        # Configure Babel
        app.config['BABEL_DEFAULT_LOCALE'] = 'en'
        app.config['BABEL_SUPPORTED_LOCALES'] = list(self.supported_languages.keys())
        app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
        
        # Initialize Babel
        self.babel = Babel(app, locale_selector=self.get_locale)
        
        # Create translations directory
        self.ensure_translations_directory()
        
        print("[OK] I18n Manager initialized with {} languages".format(len(self.supported_languages)))
    
    def get_locale(self):
        """Determine the best locale to use"""
        # 1. Check session
        if 'language' in session:
            lang = session['language']
            if lang in self.supported_languages:
                return lang
        
        # 2. Check user preferences from database
        # (implement if user authentication is available)
        
        # 3. Check browser language
        browser_lang = request.accept_languages.best_match(list(self.supported_languages.keys()))
        if browser_lang:
            return browser_lang
        
        # 4. Default to English
        return 'en'
    
    def set_language(self, language_code):
        """Set user's preferred language"""
        if language_code in self.supported_languages:
            session['language'] = language_code
            return True
        return False
    
    def get_current_language(self):
        """Get current language code"""
        return self.get_locale()
    
    def get_language_name(self, lang_code=None):
        """Get language name"""
        if lang_code is None:
            lang_code = self.get_current_language()
        return self.supported_languages.get(lang_code, {}).get('name', 'English')
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return self.supported_languages
    
    def ensure_translations_directory(self):
        """Create translations directory structure"""
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
        os.makedirs(base_dir, exist_ok=True)
        
        # Create language-specific translations
        for lang_code in self.supported_languages.keys():
            self.create_translation_file(lang_code)
    
    def create_translation_file(self, lang_code):
        """Create translation JSON file for a language"""
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
        filepath = os.path.join(base_dir, f'{lang_code}.json')
        
        if not os.path.exists(filepath):
            translations = self.get_default_translations(lang_code)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
    
    def get_default_translations(self, lang_code):
        """Get default translations for a language"""
        
        translations = {
            'en': {
                # Interface
                'app_title': 'EduBot - Smart Student Assistant',
                'app_subtitle': 'Your AI-powered study companion',
                'welcome_title': 'Welcome to EduBot!',
                'welcome_message': 'Your AI-powered study companion with 30+ smart features',
                
                # Chat
                'type_message': 'Type anything...',
                'send': 'Send',
                'clear_chat': 'Clear Chat',
                'download_history': 'Download History',
                'settings': 'Settings',
                'online': 'Online',
                
                # Features
                'quick_actions': 'Quick Actions',
                'academics': 'Academics',
                'campus': 'Campus',
                'career': 'Career',
                'admin': 'Admin',
                
                # Academic Actions
                'view_courses': 'View Courses',
                'exam_schedule': 'Exam Schedule',
                'my_assignments': 'My Assignments',
                'check_attendance': 'Check Attendance',
                
                # Campus Actions
                'library_hours': 'Library Hours',
                'canteen_menu': 'Canteen Menu',
                'bus_schedule': 'Bus Schedule',
                'hostel_info': 'Hostel Info',
                
                # Career Actions
                'placements': 'Placements',
                'internships': 'Internships',
                'project_ideas': 'Project Ideas',
                
                # Messages
                'connection_error': 'Connection error. Please check your internet.',
                'error_occurred': 'Sorry, I encountered an error.',
                'chat_cleared': 'Chat history cleared!',
                'language_changed': 'Language changed successfully!',
                
                # Stats
                'conversations': 'Conversations',
                'students_today': 'Students Today',
                'satisfaction': 'Satisfaction',
            },
            
            'hi': {
                # Interface
                'app_title': 'एडुबॉट - स्मार्ट छात्र सहायक',
                'app_subtitle': 'आपका AI-संचालित अध्ययन साथी',
                'welcome_title': 'एडुबॉट में आपका स्वागत है!',
                'welcome_message': '30+ स्मार्ट सुविधाओं के साथ आपका AI-संचालित अध्ययन साथी',
                
                # Chat
                'type_message': 'कुछ भी टाइप करें...',
                'send': 'भेजें',
                'clear_chat': 'चैट साफ़ करें',
                'download_history': 'इतिहास डाउनलोड करें',
                'settings': 'सेटिंग्स',
                'online': 'ऑनलाइन',
                
                # Features
                'quick_actions': 'त्वरित कार्य',
                'academics': 'शैक्षणिक',
                'campus': 'परिसर',
                'career': 'करियर',
                'admin': 'प्रशासन',
                
                # Academic Actions
                'view_courses': 'पाठ्यक्रम देखें',
                'exam_schedule': 'परीक्षा कार्यक्रम',
                'my_assignments': 'मेरे असाइनमेंट',
                'check_attendance': 'उपस्थिति जांचें',
                
                # Campus Actions
                'library_hours': 'पुस्तकालय समय',
                'canteen_menu': 'कैंटीन मेनू',
                'bus_schedule': 'बस समय-सारणी',
                'hostel_info': 'हॉस्टल जानकारी',
                
                # Career Actions
                'placements': 'प्लेसमेंट',
                'internships': 'इंटर्नशिप',
                'project_ideas': 'परियोजना विचार',
                
                # Messages
                'connection_error': 'कनेक्शन त्रुटि। कृपया अपना इंटरनेट जांचें।',
                'error_occurred': 'क्षमा करें, एक त्रुटि हुई।',
                'chat_cleared': 'चैट इतिहास साफ़ हो गया!',
                'language_changed': 'भाषा सफलतापूर्वक बदल गई!',
                
                # Stats
                'conversations': 'वार्तालाप',
                'students_today': 'आज के छात्र',
                'satisfaction': 'संतुष्टि',
            },
            
            'es': {
                # Interface
                'app_title': 'EduBot - Asistente Inteligente para Estudiantes',
                'app_subtitle': 'Tu compañero de estudio con IA',
                'welcome_title': '¡Bienvenido a EduBot!',
                'welcome_message': 'Tu compañero de estudio con IA con más de 30 funciones inteligentes',
                
                # Chat
                'type_message': 'Escribe cualquier cosa...',
                'send': 'Enviar',
                'clear_chat': 'Limpiar Chat',
                'download_history': 'Descargar Historial',
                'settings': 'Configuración',
                'online': 'En línea',
                
                # Features
                'quick_actions': 'Acciones Rápidas',
                'academics': 'Académicos',
                'campus': 'Campus',
                'career': 'Carrera',
                'admin': 'Administración',
                
                # Academic Actions
                'view_courses': 'Ver Cursos',
                'exam_schedule': 'Horario de Exámenes',
                'my_assignments': 'Mis Tareas',
                'check_attendance': 'Verificar Asistencia',
                
                # Campus Actions
                'library_hours': 'Horario de Biblioteca',
                'canteen_menu': 'Menú del Comedor',
                'bus_schedule': 'Horario de Autobús',
                'hostel_info': 'Información del Hostal',
                
                # Career Actions
                'placements': 'Colocaciones',
                'internships': 'Pasantías',
                'project_ideas': 'Ideas de Proyectos',
                
                # Messages
                'connection_error': 'Error de conexión. Verifica tu internet.',
                'error_occurred': 'Lo siento, ocurrió un error.',
                'chat_cleared': '¡Historial de chat limpiado!',
                'language_changed': '¡Idioma cambiado exitosamente!',
                
                # Stats
                'conversations': 'Conversaciones',
                'students_today': 'Estudiantes Hoy',
                'satisfaction': 'Satisfacción',
            }
        }
        
        return translations.get(lang_code, translations['en'])
    
    def translate(self, key, lang_code=None):
        """Translate a key to current or specified language"""
        if lang_code is None:
            lang_code = self.get_current_language()
        
        # Load translations from file
        base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'translations')
        filepath = os.path.join(base_dir, f'{lang_code}.json')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                translations = json.load(f)
                return translations.get(key, key)
        except:
            return key
    
    def translate_aiml_response(self, response, target_lang):
        """
        Translate AIML response to target language
        This is a simple implementation - for production, use Google Translate API
        """
        if target_lang == 'en':
            return response
        
        # Simple keyword-based translation for common responses
        translations = {
            'hi': {
                'Hello': 'नमस्ते',
                'How can I help you': 'मैं आपकी कैसे मदद कर सकता हूं',
                'Good morning': 'शुभ प्रभात',
                'Good afternoon': 'शुभ दोपहर',
                'Good evening': 'शुभ संध्या',
                'Thank you': 'धन्यवाद',
                'Welcome': 'स्वागत है',
                'Goodbye': 'अलविदा',
            },
            'es': {
                'Hello': 'Hola',
                'How can I help you': 'Cómo puedo ayudarte',
                'Good morning': 'Buenos días',
                'Good afternoon': 'Buenas tardes',
                'Good evening': 'Buenas noches',
                'Thank you': 'Gracias',
                'Welcome': 'Bienvenido',
                'Goodbye': 'Adiós',
            }
        }
        
        lang_translations = translations.get(target_lang, {})
        for en_word, translated_word in lang_translations.items():
            response = response.replace(en_word, translated_word)
        
        return response


# Global i18n manager instance
i18n_manager = I18nManager()


def init_i18n(app):
    """Initialize i18n with Flask app"""
    global i18n_manager
    i18n_manager.init_app(app)
    return i18n_manager


def get_i18n():
    """Get i18n manager instance"""
    return i18n_manager


# Helper functions
def _(key):
    """Shorthand for translate"""
    return i18n_manager.translate(key)


def get_current_language():
    """Get current language code"""
    return i18n_manager.get_current_language()


def set_language(lang_code):
    """Set current language"""
    return i18n_manager.set_language(lang_code)

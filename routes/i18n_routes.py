"""
I18n API Routes
Language switching and translation endpoints
"""

from flask import Blueprint, request, session, jsonify
from backend.i18n_manager import get_i18n, set_language, get_current_language
from backend.utils import success_response, error_response

i18n_bp = Blueprint('i18n', __name__)


@i18n_bp.route('/languages', methods=['GET'])
def get_languages():
    """Get list of supported languages"""
    try:
        i18n = get_i18n()
        languages = i18n.get_supported_languages()
        current_lang = get_current_language()
        
        return success_response({
            'languages': languages,
            'current': current_lang,
            'current_name': i18n.get_language_name(current_lang)
        })
    except Exception as e:
        return error_response(str(e), 500)


@i18n_bp.route('/set-language', methods=['POST'])
def set_user_language():
    """Set user's preferred language"""
    try:
        data = request.get_json()
        language_code = data.get('language')
        
        if not language_code:
            return error_response('Language code required', 400)
        
        if set_language(language_code):
            i18n = get_i18n()
            return success_response({
                'language': language_code,
                'language_name': i18n.get_language_name(language_code),
                'message': 'Language changed successfully!'
            })
        else:
            return error_response('Invalid language code', 400)
            
    except Exception as e:
        return error_response(str(e), 500)


@i18n_bp.route('/translate', methods=['POST'])
def translate_text():
    """Translate a key or text"""
    try:
        data = request.get_json()
        key = data.get('key')
        target_lang = data.get('target_lang', get_current_language())
        
        if not key:
            return error_response('Key required', 400)
        
        i18n = get_i18n()
        translated = i18n.translate(key, target_lang)
        
        return success_response({
            'original': key,
            'translated': translated,
            'language': target_lang
        })
        
    except Exception as e:
        return error_response(str(e), 500)


@i18n_bp.route('/current', methods=['GET'])
def get_current():
    """Get current language info"""
    try:
        i18n = get_i18n()
        current_lang = get_current_language()
        
        return success_response({
            'language': current_lang,
            'language_name': i18n.get_language_name(current_lang),
            'flag': i18n.supported_languages[current_lang]['flag']
        })
        
    except Exception as e:
        return error_response(str(e), 500)

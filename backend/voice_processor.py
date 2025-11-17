"""
Voice Processor for Hybrid Voice Chatbot
Handles Speech-to-Text and Text-to-Speech operations
"""
import os
from gtts import gTTS
import tempfile
from datetime import datetime

# Try to import pyttsx3 (optional dependency)
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False
    print("⚠ pyttsx3 not available - using gTTS only")


class VoiceProcessor:
    """Handles voice input/output processing"""
    
    def __init__(self, language='en', tts_engine='gtts'):
        self.language = language
        self.tts_engine = tts_engine
        self.temp_dir = tempfile.gettempdir()
    
    def text_to_speech(self, text, slow=False):
        """Convert text to speech audio file"""
        try:
            if self.tts_engine == 'gtts':
                return self._gtts_convert(text, slow)
            elif self.tts_engine == 'pyttsx3':
                return self._pyttsx3_convert(text)
            else:
                raise ValueError(f"Unsupported TTS engine: {self.tts_engine}")
                
        except Exception as e:
            print(f"Error in text-to-speech: {str(e)}")
            return None
    
    def _gtts_convert(self, text, slow=False):
        """Convert text to speech using gTTS"""
        try:
            # Create TTS object
            tts = gTTS(text=text, lang=self.language, slow=slow)
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_{timestamp}.mp3"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Save audio file
            tts.save(filepath)
            
            print(f"✓ Created TTS audio: {filename}")
            return filepath
            
        except Exception as e:
            print(f"Error in gTTS conversion: {str(e)}")
            return None
    
    def _pyttsx3_convert(self, text):
        """Convert text to speech using pyttsx3 (offline)"""
        if not PYTTSX3_AVAILABLE:
            print("⚠ pyttsx3 not available, falling back to gTTS")
            return self._gtts_convert(text, slow=False)
        
        try:
            engine = pyttsx3.init()
            
            # Set properties
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 0.9)  # Volume
            
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tts_{timestamp}.wav"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Save to file
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            
            print(f"✓ Created TTS audio: {filename}")
            return filepath
            
        except Exception as e:
            print(f"Error in pyttsx3 conversion: {str(e)}")
            return None
    
    def speech_to_text_info(self):
        """
        Provide information about speech-to-text setup
        Note: Actual STT is handled by Web Speech API in browser
        """
        return {
            'method': 'Web Speech API (browser-based)',
            'note': 'Speech recognition is handled client-side using browser capabilities',
            'fallback': 'Python SpeechRecognition library available for server-side processing',
            'supported_languages': ['en-US', 'en-GB', 'hi-IN', 'es-ES', 'fr-FR']
        }
    
    def process_audio_file(self, audio_file_path):
        """Process uploaded audio file for speech recognition"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            
            # Load audio file
            with sr.AudioFile(audio_file_path) as source:
                audio_data = recognizer.record(source)
            
            # Recognize speech
            text = recognizer.recognize_google(audio_data, language=self.language)
            
            print(f"✓ Transcribed audio: {text}")
            return text
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {str(e)}")
            return None
        except Exception as e:
            print(f"Error processing audio file: {str(e)}")
            return None
    
    def validate_audio_file(self, filepath, max_size_mb=10):
        """Validate uploaded audio file"""
        try:
            if not os.path.exists(filepath):
                return False, "File does not exist"
            
            # Check file size
            file_size = os.path.getsize(filepath)
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size > max_size_bytes:
                return False, f"File too large. Max size: {max_size_mb}MB"
            
            # Check file extension
            valid_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext not in valid_extensions:
                return False, f"Invalid file type. Supported: {', '.join(valid_extensions)}"
            
            return True, "Valid audio file"
            
        except Exception as e:
            return False, f"Error validating file: {str(e)}"
    
    def cleanup_temp_files(self, older_than_hours=24):
        """Clean up old temporary audio files"""
        try:
            import time
            
            current_time = time.time()
            deleted_count = 0
            
            for filename in os.listdir(self.temp_dir):
                if filename.startswith('tts_'):
                    filepath = os.path.join(self.temp_dir, filename)
                    file_age = current_time - os.path.getctime(filepath)
                    
                    # Delete if older than specified hours
                    if file_age > (older_than_hours * 3600):
                        os.remove(filepath)
                        deleted_count += 1
            
            if deleted_count > 0:
                print(f"✓ Cleaned up {deleted_count} temporary audio files")
            
            return deleted_count
            
        except Exception as e:
            print(f"Error cleaning up temp files: {str(e)}")
            return 0
    
    def get_voice_stats(self):
        """Get voice processing statistics"""
        try:
            temp_files = [f for f in os.listdir(self.temp_dir) if f.startswith('tts_')]
            
            return {
                'tts_engine': self.tts_engine,
                'language': self.language,
                'temp_files_count': len(temp_files),
                'temp_directory': self.temp_dir
            }
            
        except Exception as e:
            print(f"Error getting voice stats: {str(e)}")
            return {}
    
    def set_language(self, language_code):
        """Change the language for voice processing"""
        supported_languages = {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'zh': 'Chinese'
        }
        
        if language_code in supported_languages:
            self.language = language_code
            print(f"✓ Language changed to: {supported_languages[language_code]}")
            return True
        else:
            print(f"✗ Unsupported language: {language_code}")
            return False
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return {
            'en': 'English',
            'hi': 'Hindi',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'zh': 'Chinese'
        }

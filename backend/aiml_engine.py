"""
AIML Engine for Hybrid Voice Chatbot
Handles AIML pattern matching and response generation
"""
import os
import aiml
from datetime import datetime


class AIMLEngine:
    """AIML response engine"""
    
    def __init__(self, aiml_dir):
        """Initialize AIML engine"""
        self.aiml_dir = aiml_dir
        self.kernel = aiml.Kernel()
        self.loaded = False
        self.load_patterns()
    
    def load_patterns(self):
        """Load all AIML pattern files"""
        try:
            if not os.path.exists(self.aiml_dir):
                os.makedirs(self.aiml_dir)
                print(f"Created AIML directory: {self.aiml_dir}")
                return False
            
            # Load all .aiml and .xml files
            pattern_files = []
            for filename in os.listdir(self.aiml_dir):
                if filename.endswith(('.aiml', '.xml')):
                    filepath = os.path.join(self.aiml_dir, filename)
                    pattern_files.append(filepath)
            
            if not pattern_files:
                print(f"[WARNING] No AIML pattern files found in {self.aiml_dir}")
                self._create_default_patterns()
                # Reload after creating defaults
                pattern_files = [
                    os.path.join(self.aiml_dir, f) 
                    for f in os.listdir(self.aiml_dir) 
                    if f.endswith(('.aiml', '.xml'))
                ]
            
            # Learn patterns
            for filepath in pattern_files:
                try:
                    self.kernel.learn(filepath)
                    print(f"[OK] Loaded AIML pattern: {os.path.basename(filepath)}")
                except Exception as e:
                    print(f"[ERROR] Error loading {filepath}: {str(e)}")
            
            self.loaded = True
            print(f"[OK] AIML Engine initialized with {len(pattern_files)} pattern files")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error loading AIML patterns: {str(e)}")
            self.loaded = False
            return False
    
    def _create_default_patterns(self):
        """Create default AIML patterns if none exist"""
        default_patterns = {
            'startup.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>LOAD AIML B</pattern>
        <template>AIML patterns loaded successfully.</template>
    </category>
</aiml>''',
            
            'greetings.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>HELLO</pattern>
        <template>Hello! I'm your hybrid voice chatbot. How can I assist you today?</template>
    </category>
    
    <category>
        <pattern>HI</pattern>
        <template>Hi there! I'm here to help. What would you like to know?</template>
    </category>
    
    <category>
        <pattern>HEY</pattern>
        <template>Hey! What can I do for you today?</template>
    </category>
    
    <category>
        <pattern>GOOD MORNING</pattern>
        <template>Good morning! How can I help you today?</template>
    </category>
    
    <category>
        <pattern>GOOD AFTERNOON</pattern>
        <template>Good afternoon! What can I assist you with?</template>
    </category>
    
    <category>
        <pattern>GOOD EVENING</pattern>
        <template>Good evening! How may I help you?</template>
    </category>
    
    <category>
        <pattern>BYE</pattern>
        <template>Goodbye! Have a great day!</template>
    </category>
    
    <category>
        <pattern>GOODBYE</pattern>
        <template>Goodbye! Feel free to come back anytime!</template>
    </category>
    
    <category>
        <pattern>SEE YOU</pattern>
        <template>See you later! Take care!</template>
    </category>
    
    <category>
        <pattern>THANK YOU</pattern>
        <template>You're welcome! Is there anything else I can help you with?</template>
    </category>
    
    <category>
        <pattern>THANKS</pattern>
        <template>You're welcome! Feel free to ask more questions!</template>
    </category>
</aiml>''',
            
            'general.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <category>
        <pattern>WHAT IS YOUR NAME</pattern>
        <template>I'm a Hybrid Voice Chatbot with learning capabilities!</template>
    </category>
    
    <category>
        <pattern>WHO ARE YOU</pattern>
        <template>I'm an AI-powered chatbot designed to help you with information and answer your questions. I can also learn from your feedback!</template>
    </category>
    
    <category>
        <pattern>WHAT CAN YOU DO</pattern>
        <template>I can answer questions, have conversations, learn from feedback, and assist you with various topics. I support both text and voice input!</template>
    </category>
    
    <category>
        <pattern>HOW ARE YOU</pattern>
        <template>I'm functioning perfectly! Ready to help you. How about you?</template>
    </category>
    
    <category>
        <pattern>HELP</pattern>
        <template>I'm here to help! You can ask me questions, have conversations, or provide feedback to help me learn. Just type or speak your question!</template>
    </category>
    
    <category>
        <pattern>WHAT IS *</pattern>
        <template>I'm searching for information about <star/>. Let me help you with that.</template>
    </category>
    
    <category>
        <pattern>HOW TO *</pattern>
        <template>To <star/>, you would typically need to follow specific steps. Could you be more specific about what you need help with?</template>
    </category>
    
    <category>
        <pattern>WHO IS *</pattern>
        <template><star/> is someone or something I can help you learn about. Could you provide more context?</template>
    </category>
    
    <category>
        <pattern>WHERE IS *</pattern>
        <template>You're asking about the location of <star/>. I can help you find that information.</template>
    </category>
    
    <category>
        <pattern>WHEN *</pattern>
        <template>Regarding when <star/>, that depends on the specific context. Can you provide more details?</template>
    </category>
    
    <category>
        <pattern>WHY *</pattern>
        <template>That's a great question about why <star/>. Let me think about that.</template>
    </category>
    
    <category>
        <pattern>*</pattern>
        <template>I'm still learning about that topic. Could you help me improve by providing more information? You can also provide feedback to help me learn!</template>
    </category>
</aiml>''',
            
            'knowledge_base.xml': '''<?xml version="1.0" encoding="UTF-8"?>
<aiml version="2.0">
    <!-- This file will be dynamically updated with approved knowledge -->
    <category>
        <pattern>KNOWLEDGE BASE</pattern>
        <template>This is where dynamically learned patterns are stored.</template>
    </category>
</aiml>'''
        }
        
        for filename, content in default_patterns.items():
            filepath = os.path.join(self.aiml_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Created default pattern: {filename}")
    
    def get_response(self, message, session_id='default'):
        """Get response for user message"""
        if not self.loaded:
            return "I'm still initializing. Please try again in a moment."
        
        try:
            # Clean and process input
            message = message.strip()
            if not message:
                return "Please provide a message."
            
            # Get response from AIML kernel
            response = self.kernel.respond(message, sessionID=session_id)
            
            # If no response, return learning mode message
            if not response or response == "":
                return "I'm still learning about that topic. Could you help me improve by providing the correct answer? Your feedback will help me learn!"
            
            return response
            
        except Exception as e:
            print(f"Error getting AIML response: {str(e)}")
            return "I encountered an error processing your message. Please try again."
    
    def add_pattern(self, pattern, template, category='custom'):
        """Add a new AIML pattern dynamically"""
        try:
            aiml_pattern = f'''
<category>
    <pattern>{pattern.upper()}</pattern>
    <template>{template}</template>
</category>'''
            
            # Add to knowledge_base.xml
            kb_file = os.path.join(self.aiml_dir, 'knowledge_base.xml')
            
            if os.path.exists(kb_file):
                # Read existing content
                with open(kb_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Insert new pattern before closing </aiml> tag
                if '</aiml>' in content:
                    content = content.replace('</aiml>', f'{aiml_pattern}\n</aiml>')
                else:
                    content += aiml_pattern
                
                # Write back
                with open(kb_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                # Reload the pattern
                self.kernel.learn(kb_file)
                print(f"[OK] Added new pattern: {pattern}")
                return True
            
            return False
            
        except Exception as e:
            print(f"Error adding pattern: {str(e)}")
            return False
    
    def reload_patterns(self):
        """Reload all AIML patterns"""
        self.kernel = aiml.Kernel()
        return self.load_patterns()
    
    def get_pattern_count(self):
        """Get count of loaded patterns"""
        try:
            return self.kernel.numCategories()
        except:
            return 0
    
    def set_predicate(self, name, value, session_id='default'):
        """Set a predicate for the session"""
        self.kernel.setPredicate(name, value, sessionID=session_id)
    
    def get_predicate(self, name, session_id='default'):
        """Get a predicate from the session"""
        return self.kernel.getPredicate(name, sessionID=session_id)

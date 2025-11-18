/**
 * Enhanced Voice Input/Output System
 * Professional speech-to-text and text-to-speech with multiple voices
 */

(function() {
    'use strict';

    class VoiceManager {
        constructor() {
            this.isListening = false;
            this.isSpeaking = false;
            this.recognition = null;
            this.synthesis = window.speechSynthesis;
            this.voices = [];
            this.selectedVoice = null;
            this.currentLanguage = 'en-US';
            
            // Voice settings
            this.settings = {
                rate: 0.9,
                pitch: 1.0,
                volume: 1.0,
                autoSpeak: true
            };
            
            this.init();
        }

        init() {
            // Check for browser support
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                console.warn('[Voice] Speech recognition not supported');
                return;
            }

            if (!('speechSynthesis' in window)) {
                console.warn('[Voice] Speech synthesis not supported');
                return;
            }

            // Initialize speech recognition
            this.initRecognition();
            
            // Load voices
            this.loadVoices();
            
            // Create voice controls UI
            this.createVoiceControls();
            
            console.log('[Voice] Manager initialized');
        }

        initRecognition() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            
            this.recognition.continuous = false;
            this.recognition.interimResults = true;
            this.recognition.maxAlternatives = 1;
            this.recognition.lang = this.currentLanguage;

            this.recognition.onstart = () => this.onRecognitionStart();
            this.recognition.onresult = (event) => this.onRecognitionResult(event);
            this.recognition.onerror = (event) => this.onRecognitionError(event);
            this.recognition.onend = () => this.onRecognitionEnd();
        }

        loadVoices() {
            this.voices = this.synthesis.getVoices();
            
            if (this.voices.length === 0) {
                this.synthesis.addEventListener('voiceschanged', () => {
                    this.voices = this.synthesis.getVoices();
                    this.selectBestVoice();
                });
            } else {
                this.selectBestVoice();
            }
        }

        selectBestVoice() {
            // Try to find the best voice for current language
            const langCode = this.currentLanguage.split('-')[0];
            
            // Priority: female voices, then any voice matching language
            let voice = this.voices.find(v => 
                v.lang.startsWith(langCode) && v.name.toLowerCase().includes('female')
            );
            
            if (!voice) {
                voice = this.voices.find(v => v.lang.startsWith(langCode));
            }
            
            if (!voice) {
                voice = this.voices[0]; // Fallback to first voice
            }
            
            this.selectedVoice = voice;
        }

        createVoiceControls() {
            // Voice settings button
            const headerActions = document.querySelector('.chat-actions');
            if (!headerActions) return;

            const voiceSettingsBtn = document.createElement('button');
            voiceSettingsBtn.className = 'icon-btn';
            voiceSettingsBtn.id = 'voiceSettingsBtn';
            voiceSettingsBtn.title = 'Voice Settings';
            voiceSettingsBtn.innerHTML = '<i class="fas fa-sliders-h"></i>';
            voiceSettingsBtn.onclick = () => this.showVoiceSettings();

            headerActions.insertBefore(voiceSettingsBtn, headerActions.children[1]);
        }

        showVoiceSettings() {
            const overlay = document.createElement('div');
            overlay.className = 'modal-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: fadeIn 0.3s ease-out;
            `;

            const modal = document.createElement('div');
            modal.className = 'voice-settings-modal modal-content';
            modal.style.cssText = `
                background: white;
                border-radius: 16px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            `;

            modal.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h2 style="margin: 0; font-size: 1.5rem; color: #1e293b;">
                        <i class="fas fa-microphone-alt" style="color: #667eea; margin-right: 0.5rem;"></i>
                        Voice Settings
                    </h2>
                    <button onclick="this.closest('.modal-overlay').remove()" 
                            style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <div class="voice-settings-content">
                    <!-- Voice Selection -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: #475569;">
                            Select Voice
                        </label>
                        <select id="voiceSelect" class="form-control" style="width: 100%; padding: 0.75rem; border-radius: 8px; border: 2px solid #e2e8f0;">
                            ${this.voices.map(voice => `
                                <option value="${voice.name}" ${voice === this.selectedVoice ? 'selected' : ''}>
                                    ${voice.name} (${voice.lang})
                                </option>
                            `).join('')}
                        </select>
                    </div>

                    <!-- Speech Rate -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: #475569;">
                            Speech Rate: <span id="rateValue">${this.settings.rate}</span>
                        </label>
                        <input type="range" id="rateSlider" min="0.5" max="2" step="0.1" value="${this.settings.rate}"
                               style="width: 100%;">
                    </div>

                    <!-- Pitch -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: #475569;">
                            Pitch: <span id="pitchValue">${this.settings.pitch}</span>
                        </label>
                        <input type="range" id="pitchSlider" min="0" max="2" step="0.1" value="${this.settings.pitch}"
                               style="width: 100%;">
                    </div>

                    <!-- Volume -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: #475569;">
                            Volume: <span id="volumeValue">${this.settings.volume}</span>
                        </label>
                        <input type="range" id="volumeSlider" min="0" max="1" step="0.1" value="${this.settings.volume}"
                               style="width: 100%;">
                    </div>

                    <!-- Auto-Speak -->
                    <div style="margin-bottom: 1.5rem;">
                        <label style="display: flex; align-items: center; cursor: pointer;">
                            <input type="checkbox" id="autoSpeakCheckbox" ${this.settings.autoSpeak ? 'checked' : ''}
                                   style="margin-right: 0.5rem; width: 20px; height: 20px;">
                            <span style="font-weight: 600; color: #475569;">Auto-speak bot responses</span>
                        </label>
                    </div>

                    <!-- Test Button -->
                    <button onclick="window.voiceManager.testVoice()" 
                            style="width: 100%; padding: 0.875rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                        <i class="fas fa-play"></i> Test Voice
                    </button>
                </div>
            `;

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // Add event listeners
            document.getElementById('voiceSelect').addEventListener('change', (e) => {
                this.selectedVoice = this.voices.find(v => v.name === e.target.value);
            });

            document.getElementById('rateSlider').addEventListener('input', (e) => {
                this.settings.rate = parseFloat(e.target.value);
                document.getElementById('rateValue').textContent = this.settings.rate;
            });

            document.getElementById('pitchSlider').addEventListener('input', (e) => {
                this.settings.pitch = parseFloat(e.target.value);
                document.getElementById('pitchValue').textContent = this.settings.pitch;
            });

            document.getElementById('volumeSlider').addEventListener('input', (e) => {
                this.settings.volume = parseFloat(e.target.value);
                document.getElementById('volumeValue').textContent = this.settings.volume;
            });

            document.getElementById('autoSpeakCheckbox').addEventListener('change', (e) => {
                this.settings.autoSpeak = e.target.checked;
            });

            overlay.onclick = (e) => {
                if (e.target === overlay) overlay.remove();
            };
        }

        // Speech Recognition Methods
        startListening() {
            if (this.isListening) return;

            try {
                this.recognition.start();
            } catch (error) {
                console.error('[Voice] Recognition start error:', error);
            }
        }

        stopListening() {
            if (!this.isListening) return;

            try {
                this.recognition.stop();
            } catch (error) {
                console.error('[Voice] Recognition stop error:', error);
            }
        }

        onRecognitionStart() {
            this.isListening = true;
            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.classList.add('recording');
                voiceBtn.innerHTML = '<i class="fas fa-stop"></i>';
            }

            // Haptic feedback
            if (window.hapticFeedback) {
                window.hapticFeedback.medium();
            }
        }

        onRecognitionResult(event) {
            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            const input = document.getElementById('messageInput');
            if (input) {
                if (finalTranscript) {
                    input.value = finalTranscript;
                    this.stopListening();
                    
                    // Auto-send after 1 second
                    setTimeout(() => {
                        if (typeof sendMessage === 'function') {
                            sendMessage();
                        }
                    }, 1000);
                } else {
                    input.value = interimTranscript;
                }
            }
        }

        onRecognitionError(event) {
            console.error('[Voice] Recognition error:', event.error);
            this.isListening = false;

            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.classList.remove('recording');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            }

            if (window.toastManager) {
                window.toastManager.show(`Voice error: ${event.error}`, 'error');
            }
        }

        onRecognitionEnd() {
            this.isListening = false;

            const voiceBtn = document.getElementById('voiceBtn');
            if (voiceBtn) {
                voiceBtn.classList.remove('recording');
                voiceBtn.innerHTML = '<i class="fas fa-microphone"></i>';
            }
        }

        // Speech Synthesis Methods
        speak(text) {
            if (this.isSpeaking) {
                this.synthesis.cancel();
            }

            const utterance = new SpeechSynthesisUtterance(text);
            utterance.voice = this.selectedVoice;
            utterance.rate = this.settings.rate;
            utterance.pitch = this.settings.pitch;
            utterance.volume = this.settings.volume;
            utterance.lang = this.currentLanguage;

            utterance.onstart = () => {
                this.isSpeaking = true;
            };

            utterance.onend = () => {
                this.isSpeaking = false;
            };

            utterance.onerror = (error) => {
                console.error('[Voice] Synthesis error:', error);
                this.isSpeaking = false;
            };

            this.synthesis.speak(utterance);
        }

        stop Speaking() {
            if (this.isSpeaking) {
                this.synthesis.cancel();
                this.isSpeaking = false;
            }
        }

        testVoice() {
            const testText = "Hello! I'm EduBot, your AI-powered smart student assistant. How can I help you today?";
            this.speak(testText);
        }

        toggleListening() {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        }

        setLanguage(langCode) {
            this.currentLanguage = langCode;
            if (this.recognition) {
                this.recognition.lang = langCode;
            }
            this.selectBestVoice();
        }
    }

    // Initialize voice manager
    let voiceManager = null;

    const initVoice = () => {
        voiceManager = new VoiceManager();
        window.voiceManager = voiceManager;
        console.log('[Voice] System initialized');
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initVoice);
    } else {
        initVoice();
    }

    // Export for global access
    window.Voice = {
        startListening: () => voiceManager?.startListening(),
        stopListening: () => voiceManager?.stopListening(),
        speak: (text) => voiceManager?.speak(text),
        stopSpeaking: () => voiceManager?.stopSpeaking(),
        toggle: () => voiceManager?.toggleListening()
    };

})();

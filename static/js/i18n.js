/**
 * Multi-Language Support (i18n) - Frontend
 * Language switcher and dynamic translation
 */

(function() {
    'use strict';

    class I18nManager {
        constructor() {
            this.currentLang = 'en';
            this.translations = {};
            this.supportedLanguages = {};
            this.init();
        }

        async init() {
            // Load supported languages
            await this.loadLanguages();
            
            // Create language switcher UI
            this.createLanguageSwitcher();
            
            // Load current language
            await this.loadCurrentLanguage();
            
            console.log('[I18n] Initialized with language:', this.currentLang);
        }

        async loadLanguages() {
            try {
                const response = await fetch('/api/i18n/languages');
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.supportedLanguages = data.data.languages;
                    this.currentLang = data.data.current;
                }
            } catch (error) {
                console.error('[I18n] Failed to load languages:', error);
            }
        }

        async loadCurrentLanguage() {
            try {
                const response = await fetch('/api/i18n/current');
                const data = await response.json();
                
                if (data.status === 'success') {
                    this.currentLang = data.data.language;
                    this.updateUI();
                }
            } catch (error) {
                console.error('[I18n] Failed to load current language:', error);
            }
        }

        createLanguageSwitcher() {
            // Create language switcher button in header
            const headerActions = document.querySelector('.chat-actions');
            if (!headerActions) return;

            const langBtn = document.createElement('button');
            langBtn.className = 'icon-btn';
            langBtn.id = 'languageBtn';
            langBtn.title = 'Change Language';
            langBtn.innerHTML = '<i class="fas fa-language"></i>';
            langBtn.onclick = () => this.showLanguageModal();

            headerActions.insertBefore(langBtn, headerActions.firstChild);
        }

        showLanguageModal() {
            // Create modal overlay
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

            // Create modal content
            const modal = document.createElement('div');
            modal.className = 'language-modal modal-content';
            modal.style.cssText = `
                background: white;
                border-radius: 16px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            `;

            // Modal header
            const header = document.createElement('div');
            header.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1.5rem;
            `;
            header.innerHTML = `
                <h2 style="margin: 0; font-size: 1.5rem; color: #1e293b;">
                    <i class="fas fa-language" style="color: #667eea; margin-right: 0.5rem;"></i>
                    Select Language
                </h2>
                <button onclick="this.closest('.modal-overlay').remove()" 
                        style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b;">
                    <i class="fas fa-times"></i>
                </button>
            `;

            // Language list
            const langList = document.createElement('div');
            langList.className = 'language-list';

            Object.entries(this.supportedLanguages).forEach(([code, info]) => {
                const langItem = document.createElement('div');
                langItem.className = 'language-item hover-lift';
                langItem.style.cssText = `
                    padding: 1rem;
                    margin-bottom: 0.75rem;
                    border-radius: 12px;
                    border: 2px solid ${code === this.currentLang ? '#667eea' : '#e2e8f0'};
                    background: ${code === this.currentLang ? '#f0f4ff' : 'white'};
                    cursor: pointer;
                    transition: all 0.3s ease;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                `;

                langItem.innerHTML = `
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span style="font-size: 2rem;">${info.flag}</span>
                        <div>
                            <div style="font-weight: 600; font-size: 1.1rem; color: #1e293b;">
                                ${info.name}
                            </div>
                            <div style="font-size: 0.875rem; color: #64748b;">
                                ${code.toUpperCase()}
                            </div>
                        </div>
                    </div>
                    ${code === this.currentLang ? '<i class="fas fa-check" style="color: #667eea; font-size: 1.5rem;"></i>' : ''}
                `;

                langItem.onclick = async () => {
                    await this.changeLanguage(code);
                    overlay.remove();
                };

                langList.appendChild(langItem);
            });

            modal.appendChild(header);
            modal.appendChild(langList);
            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            // Close on overlay click
            overlay.onclick = (e) => {
                if (e.target === overlay) {
                    overlay.remove();
                }
            };
        }

        async changeLanguage(langCode) {
            try {
                const response = await fetch('/api/i18n/set-language', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ language: langCode })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    this.currentLang = langCode;
                    this.updateUI();

                    // Show success toast
                    if (window.toastManager) {
                        window.toastManager.show(
                            `Language changed to ${data.data.language_name}`,
                            'success'
                        );
                    }

                    // Reload page to apply translations
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                }
            } catch (error) {
                console.error('[I18n] Failed to change language:', error);
                if (window.toastManager) {
                    window.toastManager.show('Failed to change language', 'error');
                }
            }
        }

        updateUI() {
            // Update language indicator
            const langBtn = document.getElementById('languageBtn');
            if (langBtn && this.supportedLanguages[this.currentLang]) {
                langBtn.title = `Current: ${this.supportedLanguages[this.currentLang].name}`;
            }
        }

        async translate(key) {
            try {
                const response = await fetch('/api/i18n/translate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ key: key })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    return data.data.translated;
                }

                return key;
            } catch (error) {
                console.error('[I18n] Translation failed:', error);
                return key;
            }
        }

        getCurrentLanguage() {
            return this.currentLang;
        }

        getLanguageName(code = null) {
            const langCode = code || this.currentLang;
            return this.supportedLanguages[langCode]?.name || 'English';
        }
    }

    // Initialize i18n manager
    let i18nManager = null;

    const initI18n = () => {
        i18nManager = new I18nManager();
        window.i18nManager = i18nManager;
        console.log('[I18n] Manager initialized');
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initI18n);
    } else {
        initI18n();
    }

    // Export for global access
    window.I18n = {
        translate: (key) => i18nManager?.translate(key),
        changeLanguage: (code) => i18nManager?.changeLanguage(code),
        getCurrentLanguage: () => i18nManager?.getCurrentLanguage(),
        getLanguageName: (code) => i18nManager?.getLanguageName(code)
    };

})();

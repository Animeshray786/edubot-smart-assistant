/**
 * Smart Autocomplete Manager
 * Provides intelligent question suggestions as user types
 */

class AutocompleteManager {
    constructor() {
        this.inputField = null;
        this.suggestionsContainer = null;
        this.debounceTimer = null;
        this.debounceDelay = 300; // ms
        this.minQueryLength = 2;
        this.maxSuggestions = 5;
        this.currentSuggestions = [];
        this.selectedIndex = -1;
        this.enabled = true;
        
        this.init();
    }
    
    init() {
        console.log('[Autocomplete] Initializing Autocomplete Manager...');
        
        // Get input field
        this.inputField = document.getElementById('messageInput');
        if (!this.inputField) {
            console.error('[Autocomplete] Message input field not found');
            return;
        }
        
        // Create suggestions container
        this.createSuggestionsContainer();
        
        // Attach event listeners
        this.attachEventListeners();
        
        console.log('[Autocomplete] Autocomplete Manager initialized');
    }
    
    createSuggestionsContainer() {
        // Create container
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.id = 'autocompleteSuggestions';
        this.suggestionsContainer.className = 'autocomplete-suggestions';
        this.suggestionsContainer.style.display = 'none';
        
        // Insert after input field
        this.inputField.parentNode.insertBefore(
            this.suggestionsContainer, 
            this.inputField.nextSibling
        );
        
        // Add CSS styles
        this.addStyles();
    }
    
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .autocomplete-suggestions {
                position: absolute;
                bottom: 70px;
                left: 20px;
                right: 20px;
                max-height: 300px;
                overflow-y: auto;
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                z-index: 1000;
                animation: slideUp 0.2s ease-out;
            }
            
            @keyframes slideUp {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .autocomplete-suggestion {
                padding: 12px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                display: flex;
                align-items: center;
                gap: 10px;
                transition: background-color 0.2s;
            }
            
            .autocomplete-suggestion:last-child {
                border-bottom: none;
            }
            
            .autocomplete-suggestion:hover,
            .autocomplete-suggestion.selected {
                background-color: #f5f5f5;
            }
            
            .autocomplete-suggestion-icon {
                font-size: 16px;
                flex-shrink: 0;
            }
            
            .autocomplete-suggestion-text {
                flex: 1;
                color: #333;
                font-size: 14px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            
            .autocomplete-suggestion-source {
                font-size: 11px;
                color: #999;
                text-transform: uppercase;
                flex-shrink: 0;
            }
            
            .autocomplete-no-results {
                padding: 16px;
                text-align: center;
                color: #999;
                font-size: 14px;
            }
        `;
        document.head.appendChild(style);
    }
    
    attachEventListeners() {
        // Input event for autocomplete
        this.inputField.addEventListener('input', (e) => {
            this.onInput(e.target.value);
        });
        
        // Keyboard navigation
        this.inputField.addEventListener('keydown', (e) => {
            if (this.suggestionsContainer.style.display === 'block') {
                this.handleKeyDown(e);
            }
        });
        
        // Click outside to close
        document.addEventListener('click', (e) => {
            if (!this.inputField.contains(e.target) && 
                !this.suggestionsContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });
        
        // Focus to show suggestions again
        this.inputField.addEventListener('focus', () => {
            const query = this.inputField.value;
            if (query.length >= this.minQueryLength) {
                this.showSuggestions();
            }
        });
    }
    
    onInput(query) {
        if (!this.enabled) return;
        
        // Clear previous timer
        if (this.debounceTimer) {
            clearTimeout(this.debounceTimer);
        }
        
        // Hide suggestions if query too short
        if (query.length < this.minQueryLength) {
            this.hideSuggestions();
            return;
        }
        
        // Debounce API call
        this.debounceTimer = setTimeout(() => {
            this.fetchSuggestions(query);
        }, this.debounceDelay);
    }
    
    async fetchSuggestions(query) {
        try {
            const response = await fetch('/api/autocomplete/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query,
                    limit: this.maxSuggestions
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.currentSuggestions = data.suggestions;
                this.renderSuggestions();
            } else {
                console.error('[Autocomplete] Error:', data.message);
                this.hideSuggestions();
            }
        } catch (error) {
            console.error('[Autocomplete] Fetch error:', error);
            this.hideSuggestions();
        }
    }
    
    renderSuggestions() {
        this.suggestionsContainer.innerHTML = '';
        this.selectedIndex = -1;
        
        if (this.currentSuggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.currentSuggestions.forEach((suggestion, index) => {
            const div = document.createElement('div');
            div.className = 'autocomplete-suggestion';
            div.dataset.index = index;
            
            div.innerHTML = `
                <span class="autocomplete-suggestion-icon">${suggestion.icon}</span>
                <span class="autocomplete-suggestion-text">${this.escapeHtml(suggestion.text)}</span>
                <span class="autocomplete-suggestion-source">${suggestion.source}</span>
            `;
            
            div.addEventListener('click', () => {
                this.selectSuggestion(index);
            });
            
            this.suggestionsContainer.appendChild(div);
        });
        
        this.showSuggestions();
    }
    
    showSuggestions() {
        this.suggestionsContainer.style.display = 'block';
    }
    
    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
        this.selectedIndex = -1;
    }
    
    handleKeyDown(e) {
        const suggestions = this.suggestionsContainer.querySelectorAll('.autocomplete-suggestion');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.selectedIndex = Math.min(this.selectedIndex + 1, suggestions.length - 1);
                this.highlightSuggestion();
                break;
                
            case 'ArrowUp':
                e.preventDefault();
                this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
                this.highlightSuggestion();
                break;
                
            case 'Enter':
                if (this.selectedIndex >= 0) {
                    e.preventDefault();
                    this.selectSuggestion(this.selectedIndex);
                }
                break;
                
            case 'Escape':
                e.preventDefault();
                this.hideSuggestions();
                break;
        }
    }
    
    highlightSuggestion() {
        const suggestions = this.suggestionsContainer.querySelectorAll('.autocomplete-suggestion');
        
        // Remove all highlights
        suggestions.forEach(s => s.classList.remove('selected'));
        
        // Highlight selected
        if (this.selectedIndex >= 0 && this.selectedIndex < suggestions.length) {
            suggestions[this.selectedIndex].classList.add('selected');
            suggestions[this.selectedIndex].scrollIntoView({ 
                block: 'nearest', 
                behavior: 'smooth' 
            });
        }
    }
    
    selectSuggestion(index) {
        if (index >= 0 && index < this.currentSuggestions.length) {
            const suggestion = this.currentSuggestions[index];
            this.inputField.value = suggestion.text;
            this.hideSuggestions();
            
            // Focus on input
            this.inputField.focus();
            
            // Add to history
            this.addToHistory(suggestion.text);
            
            // Haptic feedback
            if (window.hapticFeedback) {
                window.hapticFeedback.light();
            }
        }
    }
    
    async addToHistory(query) {
        try {
            await fetch('/api/autocomplete/add-history', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });
        } catch (error) {
            console.error('[Autocomplete] Error adding to history:', error);
        }
    }
    
    async getCategorySuggestions(category) {
        try {
            const response = await fetch(`/api/autocomplete/category/${category}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                return data.suggestions;
            }
            
            return [];
        } catch (error) {
            console.error('[Autocomplete] Error getting category suggestions:', error);
            return [];
        }
    }
    
    async getTrendingQueries() {
        try {
            const response = await fetch('/api/autocomplete/trending');
            const data = await response.json();
            
            if (data.status === 'success') {
                return data.trending;
            }
            
            return [];
        } catch (error) {
            console.error('[Autocomplete] Error getting trending queries:', error);
            return [];
        }
    }
    
    enable() {
        this.enabled = true;
        console.log('[Autocomplete] Autocomplete enabled');
    }
    
    disable() {
        this.enabled = false;
        this.hideSuggestions();
        console.log('[Autocomplete] Autocomplete disabled');
    }
    
    toggle() {
        this.enabled = !this.enabled;
        if (!this.enabled) {
            this.hideSuggestions();
        }
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize global instance
window.autocompleteManager = new AutocompleteManager();

console.log('[Autocomplete] Autocomplete script loaded');

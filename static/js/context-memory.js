/**
 * Context Memory Manager
 * Manages conversation context across sessions using SessionStorage, IndexedDB, and API
 */

class ContextMemoryManager {
    constructor() {
        this.sessionId = null;
        this.contextData = [];
        this.maxLocalMessages = 50; // Maximum messages in local storage
        this.autoSaveInterval = 30000; // Auto-save every 30 seconds
        this.dbName = 'EduBotContextDB';
        this.dbVersion = 1;
        this.storeName = 'conversations';
        this.db = null;
        
        this.init();
    }
    
    async init() {
        console.log('[Context] Initializing Context Memory Manager...');
        
        // Get or create session ID
        await this.initSessionId();
        
        // Initialize IndexedDB
        await this.initIndexedDB();
        
        // Try to load existing context
        await this.loadContext();
        
        // Start auto-save
        this.startAutoSave();
        
        // Listen for page unload to save context
        window.addEventListener('beforeunload', () => {
            this.saveContext();
        });
        
        console.log('[Context] Context Memory Manager initialized');
    }
    
    async initSessionId() {
        try {
            // Try to get session ID from API
            const response = await fetch('/api/context/session-id');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.sessionId = data.session_id;
                console.log('[Context] Session ID:', this.sessionId);
            } else {
                // Generate local session ID
                this.sessionId = this.generateSessionId();
                console.log('[Context] Generated local session ID:', this.sessionId);
            }
        } catch (error) {
            console.error('[Context] Error getting session ID:', error);
            this.sessionId = this.generateSessionId();
        }
    }
    
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    async initIndexedDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);
            
            request.onerror = () => {
                console.error('[Context] IndexedDB error:', request.error);
                reject(request.error);
            };
            
            request.onsuccess = () => {
                this.db = request.result;
                console.log('[Context] IndexedDB initialized');
                resolve();
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Create object store if not exists
                if (!db.objectStoreNames.contains(this.storeName)) {
                    const objectStore = db.createObjectStore(this.storeName, { 
                        keyPath: 'session_id' 
                    });
                    objectStore.createIndex('timestamp', 'timestamp', { unique: false });
                    console.log('[Context] Created object store:', this.storeName);
                }
            };
        });
    }
    
    async loadContext() {
        console.log('[Context] Loading context...');
        
        // Try to load from API first
        const apiContext = await this.loadFromAPI();
        
        if (apiContext && apiContext.length > 0) {
            this.contextData = apiContext;
            console.log(`[Context] Loaded ${apiContext.length} messages from API`);
            
            // Restore messages to UI
            this.restoreMessagesToUI();
            return;
        }
        
        // Try to load from IndexedDB
        const localContext = await this.loadFromIndexedDB();
        
        if (localContext && localContext.length > 0) {
            this.contextData = localContext;
            console.log(`[Context] Loaded ${localContext.length} messages from IndexedDB`);
            
            // Restore messages to UI
            this.restoreMessagesToUI();
            
            // Sync to API
            await this.saveToAPI();
        } else {
            console.log('[Context] No existing context found');
        }
    }
    
    async loadFromAPI() {
        try {
            const response = await fetch('/api/context/load');
            const data = await response.json();
            
            if (data.status === 'success' && data.has_context) {
                return data.data.context_data || [];
            }
            
            return [];
        } catch (error) {
            console.error('[Context] Error loading from API:', error);
            return [];
        }
    }
    
    async loadFromIndexedDB() {
        if (!this.db) return [];
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readonly');
            const objectStore = transaction.objectStore(this.storeName);
            const request = objectStore.get(this.sessionId);
            
            request.onsuccess = () => {
                const result = request.result;
                resolve(result ? result.messages : []);
            };
            
            request.onerror = () => {
                console.error('[Context] Error loading from IndexedDB:', request.error);
                resolve([]);
            };
        });
    }
    
    async saveContext() {
        console.log('[Context] Saving context...');
        
        // Save to IndexedDB
        await this.saveToIndexedDB();
        
        // Save to API
        await this.saveToAPI();
    }
    
    async saveToIndexedDB() {
        if (!this.db) return;
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readwrite');
            const objectStore = transaction.objectStore(this.storeName);
            
            const data = {
                session_id: this.sessionId,
                messages: this.contextData,
                timestamp: new Date().toISOString()
            };
            
            const request = objectStore.put(data);
            
            request.onsuccess = () => {
                console.log('[Context] Saved to IndexedDB');
                resolve();
            };
            
            request.onerror = () => {
                console.error('[Context] Error saving to IndexedDB:', request.error);
                reject(request.error);
            };
        });
    }
    
    async saveToAPI() {
        try {
            const response = await fetch('/api/context/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: this.contextData
                })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                console.log('[Context] Saved to API');
            } else {
                console.error('[Context] Error saving to API:', data.message);
            }
        } catch (error) {
            console.error('[Context] Error saving to API:', error);
        }
    }
    
    addMessage(sender, text, timestamp = null) {
        const message = {
            sender: sender,
            text: text,
            timestamp: timestamp || new Date().toISOString()
        };
        
        this.contextData.push(message);
        
        // Limit context size
        if (this.contextData.length > this.maxLocalMessages) {
            this.contextData = this.contextData.slice(-this.maxLocalMessages);
        }
    }
    
    async clearContext() {
        console.log('[Context] Clearing context...');
        
        this.contextData = [];
        
        // Clear from IndexedDB
        await this.clearFromIndexedDB();
        
        // Clear from API
        await this.clearFromAPI();
    }
    
    async clearFromIndexedDB() {
        if (!this.db) return;
        
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([this.storeName], 'readwrite');
            const objectStore = transaction.objectStore(this.storeName);
            const request = objectStore.delete(this.sessionId);
            
            request.onsuccess = () => {
                console.log('[Context] Cleared from IndexedDB');
                resolve();
            };
            
            request.onerror = () => {
                console.error('[Context] Error clearing IndexedDB:', request.error);
                reject(request.error);
            };
        });
    }
    
    async clearFromAPI() {
        try {
            const response = await fetch('/api/context/clear', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                console.log('[Context] Cleared from API');
            } else {
                console.error('[Context] Error clearing from API:', data.message);
            }
        } catch (error) {
            console.error('[Context] Error clearing from API:', error);
        }
    }
    
    restoreMessagesToUI() {
        console.log('[Context] Restoring messages to UI...');
        
        const messagesContainer = document.getElementById('messagesContainer');
        if (!messagesContainer) return;
        
        // Clear existing messages
        messagesContainer.innerHTML = '';
        
        // Hide welcome screen if there are messages
        const welcomeScreen = document.getElementById('welcomeScreen');
        if (welcomeScreen && this.contextData.length > 0) {
            welcomeScreen.style.display = 'none';
        }
        
        // Restore each message
        this.contextData.forEach(msg => {
            if (window.addMessage) {
                // Pass false as saveToContext to avoid re-saving
                window.addMessage(msg.text, msg.sender, [], false);
            }
        });
        
        console.log(`[Context] Restored ${this.contextData.length} messages to UI`);
        
        // Show toast notification
        if (window.toastManager && this.contextData.length > 0) {
            window.toastManager.show(
                `Restored ${this.contextData.length} messages from previous session`, 
                'success', 
                3000
            );
        }
    }
    
    startAutoSave() {
        setInterval(() => {
            if (this.contextData.length > 0) {
                this.saveContext();
            }
        }, this.autoSaveInterval);
        
        console.log(`[Context] Auto-save enabled (every ${this.autoSaveInterval / 1000}s)`);
    }
    
    async getContextSummary() {
        try {
            const response = await fetch('/api/context/summary');
            const data = await response.json();
            
            if (data.status === 'success') {
                return data.summary;
            }
            
            return null;
        } catch (error) {
            console.error('[Context] Error getting summary:', error);
            return null;
        }
    }
    
    async getContextKeywords(topN = 10) {
        try {
            const response = await fetch(`/api/context/keywords?top_n=${topN}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                return data.keywords;
            }
            
            return [];
        } catch (error) {
            console.error('[Context] Error getting keywords:', error);
            return [];
        }
    }
    
    getRecentMessages(limit = 10) {
        return this.contextData.slice(-limit);
    }
    
    getMessageCount() {
        return this.contextData.length;
    }
    
    hasContext() {
        return this.contextData.length > 0;
    }
    
    async exportContext(format = 'json') {
        const data = {
            session_id: this.sessionId,
            messages: this.contextData,
            message_count: this.contextData.length,
            exported_at: new Date().toISOString()
        };
        
        if (format === 'json') {
            const blob = new Blob([JSON.stringify(data, null, 2)], { 
                type: 'application/json' 
            });
            this.downloadFile(blob, `context_${this.sessionId}.json`);
        } else if (format === 'txt') {
            let text = `=== Context Export ===\n`;
            text += `Session ID: ${this.sessionId}\n`;
            text += `Message Count: ${this.contextData.length}\n`;
            text += `Exported: ${new Date().toLocaleString()}\n\n`;
            
            this.contextData.forEach((msg, index) => {
                text += `[${index + 1}] ${msg.sender.toUpperCase()}: ${msg.text}\n`;
                text += `    Time: ${new Date(msg.timestamp).toLocaleString()}\n\n`;
            });
            
            const blob = new Blob([text], { type: 'text/plain' });
            this.downloadFile(blob, `context_${this.sessionId}.txt`);
        }
    }
    
    downloadFile(blob, filename) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize global instance
window.contextMemory = new ContextMemoryManager();

console.log('[Context] Context Memory script loaded');

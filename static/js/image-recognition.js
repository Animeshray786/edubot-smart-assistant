/**
 * Image Recognition Manager
 * Handles image uploads, OCR with Tesseract.js, and image analysis
 */

class ImageRecognitionManager {
    constructor() {
        this.uploadButton = null;
        this.fileInput = null;
        this.tesseractWorker = null;
        this.isProcessing = false;
        this.maxFileSize = 10 * 1024 * 1024; // 10MB
        this.allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp', 'image/bmp'];
        
        this.init();
    }
    
    async init() {
        console.log('[Image] Initializing Image Recognition Manager...');
        
        // Create upload button
        this.createUploadButton();
        
        // Create file input
        this.createFileInput();
        
        // Load Tesseract.js
        await this.loadTesseract();
        
        console.log('[Image] Image Recognition Manager initialized');
    }
    
    createUploadButton() {
        // Add upload button to input area (next to voice button)
        const inputArea = document.querySelector('.chat-input-area');
        if (!inputArea) {
            console.error('[Image] Input area not found');
            return;
        }
        
        const voiceBtn = document.getElementById('voiceBtn');
        if (!voiceBtn) return;
        
        this.uploadButton = document.createElement('button');
        this.uploadButton.id = 'imageUploadBtn';
        this.uploadButton.className = 'chat-input-btn ripple';
        this.uploadButton.innerHTML = '<i class="fas fa-image"></i>';
        this.uploadButton.title = 'Upload Image for OCR';
        this.uploadButton.onclick = () => this.openFileDialog();
        
        // Insert before voice button
        voiceBtn.parentNode.insertBefore(this.uploadButton, voiceBtn);
    }
    
    createFileInput() {
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.accept = 'image/*';
        this.fileInput.style.display = 'none';
        this.fileInput.onchange = (e) => this.handleFileSelect(e);
        
        document.body.appendChild(this.fileInput);
    }
    
    async loadTesseract() {
        try {
            // Check if Tesseract is already loaded
            if (window.Tesseract) {
                console.log('[Image] Tesseract.js already loaded');
                await this.initTesseractWorker();
                return;
            }
            
            // Load Tesseract.js from CDN
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/tesseract.js@4/dist/tesseract.min.js';
            script.onload = async () => {
                console.log('[Image] Tesseract.js loaded');
                await this.initTesseractWorker();
            };
            script.onerror = () => {
                console.error('[Image] Failed to load Tesseract.js');
                if (window.toastManager) {
                    window.toastManager.show('OCR library failed to load', 'error');
                }
            };
            
            document.head.appendChild(script);
            
        } catch (error) {
            console.error('[Image] Error loading Tesseract:', error);
        }
    }
    
    async initTesseractWorker() {
        try {
            if (!window.Tesseract) {
                console.error('[Image] Tesseract not available');
                return;
            }
            
            this.tesseractWorker = await Tesseract.createWorker({
                logger: (m) => {
                    if (m.status === 'recognizing text') {
                        console.log(`[Image] OCR Progress: ${(m.progress * 100).toFixed(0)}%`);
                    }
                }
            });
            
            await this.tesseractWorker.loadLanguage('eng');
            await this.tesseractWorker.initialize('eng');
            
            console.log('[Image] Tesseract worker initialized');
            
        } catch (error) {
            console.error('[Image] Error initializing Tesseract worker:', error);
        }
    }
    
    openFileDialog() {
        this.fileInput.click();
    }
    
    async handleFileSelect(event) {
        const file = event.target.files[0];
        
        if (!file) return;
        
        // Validate file
        const validation = this.validateFile(file);
        if (!validation.valid) {
            if (window.toastManager) {
                window.toastManager.show(validation.error, 'error');
            }
            return;
        }
        
        // Process image
        await this.processImage(file);
        
        // Reset input
        event.target.value = '';
    }
    
    validateFile(file) {
        // Check file type
        if (!this.allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: 'Invalid file type. Please upload an image (PNG, JPG, GIF, WebP, BMP)'
            };
        }
        
        // Check file size
        if (file.size > this.maxFileSize) {
            return {
                valid: false,
                error: `File too large. Maximum size is ${this.maxFileSize / (1024 * 1024)}MB`
            };
        }
        
        return { valid: true };
    }
    
    async processImage(file) {
        if (this.isProcessing) {
            if (window.toastManager) {
                window.toastManager.show('Already processing an image', 'warning');
            }
            return;
        }
        
        this.isProcessing = true;
        
        try {
            // Show loading state
            const loadingOverlay = this.showLoadingOverlay('Processing image...');
            
            // Create image preview
            const preview = await this.createImagePreview(file);
            
            // Add preview to chat
            this.addImageMessage(preview);
            
            // Extract text with OCR
            loadingOverlay.querySelector('.loading-text').textContent = 'Extracting text with OCR...';
            
            const ocrResult = await this.extractText(file);
            
            // Hide loading
            document.body.removeChild(loadingOverlay);
            
            // Display result
            this.displayOCRResult(ocrResult);
            
            // Haptic feedback
            if (window.hapticFeedback) {
                window.hapticFeedback.success();
            }
            
        } catch (error) {
            console.error('[Image] Error processing image:', error);
            
            if (window.toastManager) {
                window.toastManager.show('Error processing image', 'error');
            }
            
        } finally {
            this.isProcessing = false;
        }
    }
    
    async createImagePreview(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                resolve(e.target.result);
            };
            
            reader.onerror = reject;
            
            reader.readAsDataURL(file);
        });
    }
    
    addImageMessage(imageDataUrl) {
        const container = document.getElementById('messagesContainer');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-user fade-in-up';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">
                    <div class="message-image-preview">
                        <img src="${imageDataUrl}" alt="Uploaded image" style="max-width: 100%; border-radius: 8px;">
                    </div>
                    <div style="margin-top: 8px; font-style: italic; color: #666;">
                        📷 Image uploaded - Extracting text...
                    </div>
                </div>
                <div class="message-time">${time}</div>
            </div>
            <span class="message-avatar scale-in"><i class="fas fa-user"></i></span>
        `;
        
        container.appendChild(messageDiv);
        
        // Scroll to bottom
        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        });
    }
    
    async extractText(file) {
        if (!this.tesseractWorker) {
            throw new Error('OCR worker not initialized');
        }
        
        try {
            const result = await this.tesseractWorker.recognize(file);
            
            return {
                text: result.data.text.trim(),
                confidence: result.data.confidence,
                success: true
            };
            
        } catch (error) {
            console.error('[Image] OCR error:', error);
            return {
                text: '',
                confidence: 0,
                success: false,
                error: error.message
            };
        }
    }
    
    displayOCRResult(result) {
        const container = document.getElementById('messagesContainer');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-bot fade-in-up';
        
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        let content;
        
        if (result.success && result.text.length > 0) {
            const confidencePercent = (result.confidence || 0).toFixed(0);
            
            content = `
                <div class="ocr-result">
                    <div style="background: #e8f5e9; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                        <strong>📝 Extracted Text:</strong>
                    </div>
                    <div style="background: #f5f5f5; padding: 12px; border-radius: 8px; font-family: monospace; white-space: pre-wrap;">
${result.text}
                    </div>
                    <div style="margin-top: 8px; font-size: 12px; color: #666;">
                        Confidence: ${confidencePercent}%
                    </div>
                    <div style="margin-top: 12px;">
                        <button class="btn btn-sm btn-primary ripple" onclick="navigator.clipboard.writeText(\`${result.text.replace(/`/g, '\\`')}\`)">
                            <i class="fas fa-copy"></i> Copy Text
                        </button>
                        <button class="btn btn-sm btn-outline-primary ripple" onclick="document.getElementById('messageInput').value = \`${result.text.replace(/`/g, '\\`')}\`; document.getElementById('messageInput').focus();">
                            <i class="fas fa-edit"></i> Use as Query
                        </button>
                    </div>
                </div>
            `;
        } else {
            content = `
                <div style="color: #f44336;">
                    ❌ No text detected in the image.
                </div>
                <div style="margin-top: 8px; font-size: 14px; color: #666;">
                    Tips: Make sure the image contains clear, readable text.
                </div>
            `;
        }
        
        messageDiv.innerHTML = `
            <span class="message-avatar scale-in"><i class="fas fa-robot"></i></span>
            <div class="message-content">
                <div class="message-bubble">
                    ${content}
                </div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        container.appendChild(messageDiv);
        
        // Scroll to bottom
        container.scrollTo({
            top: container.scrollHeight,
            behavior: 'smooth'
        });
        
        // Save to context memory
        if (window.contextMemory) {
            window.contextMemory.addMessage('bot', `OCR Result: ${result.text || 'No text detected'}`);
        }
        
        // Auto-speak result
        if (result.success && result.text && window.voiceManager && window.voiceManager.settings.autoSpeak) {
            window.voiceManager.speak(`Extracted text: ${result.text}`);
        }
    }
    
    showLoadingOverlay(message = 'Processing...') {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner"></div>
                <div class="loading-text">${message}</div>
            </div>
        `;
        
        // Add CSS if not exists
        if (!document.getElementById('image-recognition-styles')) {
            const style = document.createElement('style');
            style.id = 'image-recognition-styles';
            style.textContent = `
                .loading-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.7);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                }
                
                .loading-content {
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    text-align: center;
                }
                
                .loading-text {
                    margin-top: 16px;
                    font-size: 16px;
                    color: #333;
                }
                
                .ocr-result .btn {
                    margin-right: 8px;
                    margin-top: 4px;
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(overlay);
        return overlay;
    }
    
    async cleanup() {
        if (this.tesseractWorker) {
            await this.tesseractWorker.terminate();
            this.tesseractWorker = null;
            console.log('[Image] Tesseract worker terminated');
        }
    }
}

// Initialize global instance
window.imageRecognition = new ImageRecognitionManager();

console.log('[Image] Image Recognition script loaded');

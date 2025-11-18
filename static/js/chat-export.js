/**
 * Chat Export System
 * Export conversation history as PDF, TXT, or JSON
 */

(function() {
    'use strict';

    class ChatExporter {
        constructor() {
            this.conversations = [];
            this.init();
        }

        init() {
            console.log('[ChatExport] Initialized');
        }

        /**
         * Collect all messages from chat
         */
        collectMessages() {
            const messagesContainer = document.getElementById('messagesContainer');
            if (!messagesContainer) return [];

            const messages = [];
            const messageElements = messagesContainer.querySelectorAll('.message:not(.message-skeleton)');

            messageElements.forEach(msgEl => {
                const isUser = msgEl.classList.contains('message-user');
                const bubbleEl = msgEl.querySelector('.message-bubble');
                const timeEl = msgEl.querySelector('.message-time');

                if (bubbleEl) {
                    messages.push({
                        sender: isUser ? 'User' : 'EduBot',
                        message: bubbleEl.textContent.trim(),
                        time: timeEl ? timeEl.textContent.trim() : new Date().toLocaleTimeString(),
                        timestamp: new Date().toISOString()
                    });
                }
            });

            return messages;
        }

        /**
         * Export as JSON
         */
        exportAsJSON() {
            const messages = this.collectMessages();
            
            if (messages.length === 0) {
                if (window.toastManager) {
                    window.toastManager.show('No messages to export!', 'warning');
                }
                return;
            }

            const exportData = {
                title: 'EduBot Conversation History',
                exportDate: new Date().toISOString(),
                messageCount: messages.length,
                messages: messages
            };

            const jsonString = JSON.stringify(exportData, null, 2);
            this.downloadFile(jsonString, 'edubot-chat-' + this.getDateString() + '.json', 'application/json');

            if (window.toastManager) {
                window.toastManager.show('Chat exported as JSON!', 'success');
            }
        }

        /**
         * Export as TXT
         */
        exportAsTXT() {
            const messages = this.collectMessages();
            
            if (messages.length === 0) {
                if (window.toastManager) {
                    window.toastManager.show('No messages to export!', 'warning');
                }
                return;
            }

            let txtContent = `
╔══════════════════════════════════════════════════════════════╗
║          EDUBOT - CONVERSATION HISTORY                       ║
╠══════════════════════════════════════════════════════════════╣
║  Export Date: ${new Date().toLocaleString()}                      
║  Total Messages: ${messages.length}                                     
╚══════════════════════════════════════════════════════════════╝

`;

            messages.forEach((msg, index) => {
                txtContent += `\n─────────────────────────────────────────────────────────────\n`;
                txtContent += `[${index + 1}] ${msg.sender} (${msg.time})\n`;
                txtContent += `─────────────────────────────────────────────────────────────\n`;
                txtContent += `${msg.message}\n`;
            });

            txtContent += `\n\n╔══════════════════════════════════════════════════════════════╗\n`;
            txtContent += `║                    END OF CONVERSATION                       ║\n`;
            txtContent += `╚══════════════════════════════════════════════════════════════╝\n`;

            this.downloadFile(txtContent, 'edubot-chat-' + this.getDateString() + '.txt', 'text/plain');

            if (window.toastManager) {
                window.toastManager.show('Chat exported as TXT!', 'success');
            }
        }

        /**
         * Export as PDF
         */
        async exportAsPDF() {
            // Check if jsPDF is available
            if (typeof jspdf === 'undefined') {
                // Load jsPDF dynamically
                await this.loadJsPDF();
            }

            const messages = this.collectMessages();
            
            if (messages.length === 0) {
                if (window.toastManager) {
                    window.toastManager.show('No messages to export!', 'warning');
                }
                return;
            }

            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();

            // Page setup
            const pageWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();
            const margin = 20;
            const maxWidth = pageWidth - (margin * 2);
            let yPosition = margin;

            // Header
            doc.setFillColor(102, 126, 234);
            doc.rect(0, 0, pageWidth, 40, 'F');
            
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(24);
            doc.setFont('helvetica', 'bold');
            doc.text('EduBot', margin, 25);
            
            doc.setFontSize(12);
            doc.setFont('helvetica', 'normal');
            doc.text('Conversation History', margin, 35);

            yPosition = 50;

            // Export info
            doc.setTextColor(100, 116, 139);
            doc.setFontSize(10);
            doc.text(`Export Date: ${new Date().toLocaleString()}`, margin, yPosition);
            yPosition += 7;
            doc.text(`Total Messages: ${messages.length}`, margin, yPosition);
            yPosition += 15;

            // Messages
            messages.forEach((msg, index) => {
                // Check if we need a new page
                if (yPosition > pageHeight - 40) {
                    doc.addPage();
                    yPosition = margin;
                }

                // Message header
                doc.setFontSize(10);
                doc.setFont('helvetica', 'bold');
                
                if (msg.sender === 'User') {
                    doc.setTextColor(37, 99, 235); // Blue for user
                } else {
                    doc.setTextColor(16, 185, 129); // Green for bot
                }
                
                doc.text(`${msg.sender} - ${msg.time}`, margin, yPosition);
                yPosition += 7;

                // Message content
                doc.setFont('helvetica', 'normal');
                doc.setTextColor(51, 65, 85);
                doc.setFontSize(9);

                const lines = doc.splitTextToSize(msg.message, maxWidth - 10);
                
                // Message bubble
                const bubbleHeight = (lines.length * 5) + 8;
                doc.setFillColor(248, 250, 252);
                doc.roundedRect(margin, yPosition - 5, maxWidth, bubbleHeight, 3, 3, 'F');
                
                doc.text(lines, margin + 5, yPosition);
                yPosition += bubbleHeight + 5;

                // Separator
                if (index < messages.length - 1) {
                    doc.setDrawColor(226, 232, 240);
                    doc.line(margin, yPosition, pageWidth - margin, yPosition);
                    yPosition += 8;
                }
            });

            // Footer
            const pageCount = doc.internal.getNumberOfPages();
            for (let i = 1; i <= pageCount; i++) {
                doc.setPage(i);
                doc.setFontSize(8);
                doc.setTextColor(148, 163, 184);
                doc.text(
                    `Page ${i} of ${pageCount} - Generated by EduBot`,
                    pageWidth / 2,
                    pageHeight - 10,
                    { align: 'center' }
                );
            }

            // Save PDF
            doc.save('edubot-chat-' + this.getDateString() + '.pdf');

            if (window.toastManager) {
                window.toastManager.show('Chat exported as PDF!', 'success');
            }
        }

        /**
         * Load jsPDF library dynamically
         */
        loadJsPDF() {
            return new Promise((resolve, reject) => {
                if (typeof jspdf !== 'undefined') {
                    resolve();
                    return;
                }

                const script = document.createElement('script');
                script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }

        /**
         * Show export modal
         */
        showExportModal() {
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
            modal.className = 'export-modal modal-content';
            modal.style.cssText = `
                background: white;
                border-radius: 16px;
                padding: 2rem;
                max-width: 500px;
                width: 90%;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            `;

            const messages = this.collectMessages();

            modal.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
                    <h2 style="margin: 0; font-size: 1.5rem; color: #1e293b;">
                        <i class="fas fa-download" style="color: #667eea; margin-right: 0.5rem;"></i>
                        Export Chat
                    </h2>
                    <button onclick="this.closest('.modal-overlay').remove()" 
                            style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #64748b;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>

                <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="color: #64748b;">Total Messages:</span>
                        <strong style="color: #1e293b;">${messages.length}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #64748b;">Export Date:</span>
                        <strong style="color: #1e293b;">${new Date().toLocaleDateString()}</strong>
                    </div>
                </div>

                <div style="display: grid; gap: 1rem;">
                    <button onclick="window.chatExporter.exportAsPDF(); this.closest('.modal-overlay').remove()"
                            class="export-btn hover-lift ripple"
                            style="padding: 1rem; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.75rem;">
                        <i class="fas fa-file-pdf" style="font-size: 1.5rem;"></i>
                        <div style="text-align: left;">
                            <div>Export as PDF</div>
                            <div style="font-size: 0.75rem; opacity: 0.9;">Formatted document with styling</div>
                        </div>
                    </button>

                    <button onclick="window.chatExporter.exportAsTXT(); this.closest('.modal-overlay').remove()"
                            class="export-btn hover-lift ripple"
                            style="padding: 1rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.75rem;">
                        <i class="fas fa-file-alt" style="font-size: 1.5rem;"></i>
                        <div style="text-align: left;">
                            <div>Export as TXT</div>
                            <div style="font-size: 0.75rem; opacity: 0.9;">Plain text format</div>
                        </div>
                    </button>

                    <button onclick="window.chatExporter.exportAsJSON(); this.closest('.modal-overlay').remove()"
                            class="export-btn hover-lift ripple"
                            style="padding: 1rem; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.75rem;">
                        <i class="fas fa-code" style="font-size: 1.5rem;"></i>
                        <div style="text-align: left;">
                            <div>Export as JSON</div>
                            <div style="font-size: 0.75rem; opacity: 0.9;">Machine-readable format</div>
                        </div>
                    </button>
                </div>
            `;

            overlay.appendChild(modal);
            document.body.appendChild(overlay);

            overlay.onclick = (e) => {
                if (e.target === overlay) overlay.remove();
            };
        }

        /**
         * Helper: Download file
         */
        downloadFile(content, filename, contentType) {
            const blob = new Blob([content], { type: contentType });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
            URL.revokeObjectURL(url);
        }

        /**
         * Helper: Get date string for filename
         */
        getDateString() {
            const now = new Date();
            return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}_${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}`;
        }
    }

    // Initialize chat exporter
    let chatExporter = null;

    const initChatExporter = () => {
        chatExporter = new ChatExporter();
        window.chatExporter = chatExporter;
        console.log('[ChatExport] System initialized');
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatExporter);
    } else {
        initChatExporter();
    }

    // Export for global access
    window.ChatExport = {
        exportPDF: () => chatExporter?.exportAsPDF(),
        exportTXT: () => chatExporter?.exportAsTXT(),
        exportJSON: () => chatExporter?.exportAsJSON(),
        showModal: () => chatExporter?.showExportModal()
    };

})();

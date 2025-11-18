/**
 * Professional Animations & Transitions Controller
 * Skeleton loaders, page transitions, micro-interactions
 */

(function() {
    'use strict';

    // ==================== SKELETON LOADER MANAGER ====================
    class SkeletonLoader {
        constructor() {
            this.activeLoaders = new Set();
        }

        /**
         * Show skeleton loader for messages
         */
        showMessageSkeleton(isUser = false) {
            const container = document.getElementById('messagesContainer');
            if (!container) return null;

            const skeleton = document.createElement('div');
            skeleton.className = `message-skeleton ${isUser ? 'user' : 'bot'}`;
            skeleton.id = `skeleton-${Date.now()}`;
            skeleton.innerHTML = `
                <div class="message-skeleton-avatar"></div>
                <div class="message-skeleton-content">
                    <div class="message-skeleton-line"></div>
                    <div class="message-skeleton-line"></div>
                    <div class="message-skeleton-line"></div>
                </div>
            `;

            container.appendChild(skeleton);
            this.activeLoaders.add(skeleton.id);
            this.scrollToBottom();

            return skeleton.id;
        }

        /**
         * Remove skeleton loader
         */
        remove(loaderId) {
            const skeleton = document.getElementById(loaderId);
            if (skeleton) {
                skeleton.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => {
                    skeleton.remove();
                    this.activeLoaders.delete(loaderId);
                }, 300);
            }
        }

        /**
         * Remove all skeleton loaders
         */
        removeAll() {
            this.activeLoaders.forEach(loaderId => this.remove(loaderId));
        }

        scrollToBottom() {
            const container = document.getElementById('messagesContainer');
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        }
    }

    // ==================== PAGE TRANSITION MANAGER ====================
    class PageTransition {
        constructor() {
            this.init();
        }

        init() {
            // Intercept navigation for smooth transitions
            document.addEventListener('click', (e) => {
                const link = e.target.closest('a');
                if (link && link.href && !link.target && !link.hasAttribute('download')) {
                    // Check if it's an internal link
                    const url = new URL(link.href);
                    if (url.origin === window.location.origin && !link.hasAttribute('data-no-transition')) {
                        e.preventDefault();
                        this.navigateTo(link.href);
                    }
                }
            });
        }

        async navigateTo(url) {
            // Add leaving animation
            document.body.classList.add('page-transition-leave');

            await new Promise(resolve => setTimeout(resolve, 400));

            // Navigate
            window.location.href = url;
        }

        addEnterAnimation() {
            document.body.classList.add('page-transition-enter');
            setTimeout(() => {
                document.body.classList.remove('page-transition-enter');
            }, 400);
        }
    }

    // ==================== TOAST NOTIFICATION SYSTEM ====================
    class ToastManager {
        constructor() {
            this.toasts = [];
            this.maxToasts = 3;
        }

        show(message, type = 'info', duration = 3000) {
            const toast = this.create(message, type);
            document.body.appendChild(toast);

            this.toasts.push(toast);
            this.manageToastStack();

            // Auto-hide after duration
            setTimeout(() => this.hide(toast), duration);

            return toast;
        }

        create(message, type) {
            const toast = document.createElement('div');
            toast.className = `toast-notification ${type}`;
            toast.innerHTML = `
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="flex-shrink: 0; font-size: 20px;">
                        ${this.getIcon(type)}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; margin-bottom: 4px;">
                            ${this.getTitle(type)}
                        </div>
                        <div style="font-size: 14px; color: #64748b;">
                            ${message}
                        </div>
                    </div>
                    <button onclick="this.closest('.toast-notification').remove()" 
                            style="background: none; border: none; font-size: 20px; cursor: pointer; color: #94a3b8;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;

            return toast;
        }

        getIcon(type) {
            const icons = {
                success: '<i class="fas fa-check-circle" style="color: #10b981;"></i>',
                error: '<i class="fas fa-exclamation-circle" style="color: #ef4444;"></i>',
                warning: '<i class="fas fa-exclamation-triangle" style="color: #f59e0b;"></i>',
                info: '<i class="fas fa-info-circle" style="color: #3b82f6;"></i>'
            };
            return icons[type] || icons.info;
        }

        getTitle(type) {
            const titles = {
                success: 'Success',
                error: 'Error',
                warning: 'Warning',
                info: 'Info'
            };
            return titles[type] || 'Notification';
        }

        hide(toast) {
            toast.classList.add('hiding');
            setTimeout(() => {
                toast.remove();
                this.toasts = this.toasts.filter(t => t !== toast);
            }, 300);
        }

        manageToastStack() {
            // Remove oldest toasts if exceeding max
            while (this.toasts.length > this.maxToasts) {
                const oldestToast = this.toasts.shift();
                this.hide(oldestToast);
            }

            // Position toasts
            this.toasts.forEach((toast, index) => {
                toast.style.top = `${20 + (index * 100)}px`;
            });
        }
    }

    // ==================== SCROLL REVEAL ANIMATIONS ====================
    class ScrollReveal {
        constructor() {
            this.elements = [];
            this.init();
        }

        init() {
            // Find all elements with scroll-reveal class
            this.observe();

            // Re-observe on dynamic content
            const observer = new MutationObserver(() => this.observe());
            observer.observe(document.body, { childList: true, subtree: true });
        }

        observe() {
            const elements = document.querySelectorAll('.scroll-reveal:not(.revealed)');
            
            if ('IntersectionObserver' in window) {
                const observer = new IntersectionObserver((entries) => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('revealed');
                            observer.unobserve(entry.target);
                        }
                    });
                }, {
                    threshold: 0.1,
                    rootMargin: '0px 0px -50px 0px'
                });

                elements.forEach(el => observer.observe(el));
            } else {
                // Fallback for browsers without IntersectionObserver
                elements.forEach(el => el.classList.add('revealed'));
            }
        }
    }

    // ==================== NUMBER COUNTER ANIMATION ====================
    class CounterAnimation {
        static animateValue(element, start, end, duration = 1000) {
            let startTime = null;
            
            const animate = (currentTime) => {
                if (!startTime) startTime = currentTime;
                const progress = Math.min((currentTime - startTime) / duration, 1);
                
                const value = Math.floor(progress * (end - start) + start);
                element.textContent = value;
                element.classList.add('counter-animation');
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    element.classList.remove('counter-animation');
                }
            };
            
            requestAnimationFrame(animate);
        }

        static animateElement(element, end, duration = 1000) {
            const start = parseInt(element.textContent) || 0;
            this.animateValue(element, start, end, duration);
        }
    }

    // ==================== RIPPLE EFFECT ====================
    class RippleEffect {
        static init() {
            document.addEventListener('click', (e) => {
                const rippleElement = e.target.closest('.ripple');
                if (rippleElement) {
                    this.create(rippleElement, e);
                }
            });
        }

        static create(element, event) {
            const rect = element.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.5);
                transform: translate(-50%, -50%) scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
                left: ${x}px;
                top: ${y}px;
            `;

            element.style.position = 'relative';
            element.style.overflow = 'hidden';
            element.appendChild(ripple);

            setTimeout(() => ripple.remove(), 600);
        }
    }

    // ==================== TYPING ANIMATION ====================
    class TypingAnimation {
        static typeText(element, text, speed = 50) {
            return new Promise((resolve) => {
                element.textContent = '';
                let index = 0;

                const type = () => {
                    if (index < text.length) {
                        element.textContent += text.charAt(index);
                        index++;
                        setTimeout(type, speed);
                    } else {
                        resolve();
                    }
                };

                type();
            });
        }

        static async typeHTML(element, html, speed = 50) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            const text = tempDiv.textContent || tempDiv.innerText;
            
            await this.typeText(element, text, speed);
        }
    }

    // ==================== SHAKE ANIMATION TRIGGER ====================
    class ShakeEffect {
        static shake(element) {
            element.classList.add('shake');
            setTimeout(() => element.classList.remove('shake'), 500);
        }

        static shakeOnError(element) {
            this.shake(element);
            if (window.hapticFeedback) {
                window.hapticFeedback.error();
            }
        }
    }

    // ==================== LOADING OVERLAY ====================
    class LoadingOverlay {
        static show(message = 'Loading...') {
            const overlay = document.createElement('div');
            overlay.id = 'loading-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                z-index: 99999;
                animation: fadeIn 0.3s ease-out;
            `;
            overlay.innerHTML = `
                <div class="spinner" style="border-color: #f3f3f3; border-top-color: #667eea;"></div>
                <div style="color: white; margin-top: 20px; font-size: 16px;">${message}</div>
            `;

            document.body.appendChild(overlay);
            return overlay;
        }

        static hide() {
            const overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.animation = 'fadeOut 0.3s ease-out';
                setTimeout(() => overlay.remove(), 300);
            }
        }
    }

    // ==================== STAGGER ANIMATION ====================
    class StaggerAnimation {
        static init(containerSelector, itemSelector) {
            const container = document.querySelector(containerSelector);
            if (!container) return;

            const items = container.querySelectorAll(itemSelector);
            items.forEach((item, index) => {
                item.classList.add('stagger-item');
                item.style.animationDelay = `${index * 0.1}s`;
            });
        }
    }

    // ==================== BUTTON ANIMATIONS ====================
    class ButtonAnimations {
        static addLoadingState(button, text = 'Loading...') {
            button.dataset.originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner-small" style="display: inline-block; margin-right: 8px;"></span>
                ${text}
            `;
        }

        static removeLoadingState(button) {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || button.innerHTML;
            delete button.dataset.originalText;
        }

        static success(button, text = 'Success!', duration = 2000) {
            const original = button.innerHTML;
            button.innerHTML = `<i class="fas fa-check"></i> ${text}`;
            button.classList.add('bounce');

            setTimeout(() => {
                button.innerHTML = original;
                button.classList.remove('bounce');
            }, duration);
        }

        static error(button, text = 'Error!', duration = 2000) {
            const original = button.innerHTML;
            button.innerHTML = `<i class="fas fa-times"></i> ${text}`;
            button.classList.add('shake');

            setTimeout(() => {
                button.innerHTML = original;
                button.classList.remove('shake');
            }, duration);
        }
    }

    // ==================== INITIALIZE ALL ANIMATIONS ====================
    const initAnimations = () => {
        // Initialize all animation systems
        window.skeletonLoader = new SkeletonLoader();
        window.pageTransition = new PageTransition();
        window.toastManager = new ToastManager();
        window.scrollReveal = new ScrollReveal();

        // Initialize ripple effect
        RippleEffect.init();

        // Add page enter animation
        window.pageTransition.addEnterAnimation();

        // Add animations to existing elements
        const buttons = document.querySelectorAll('button:not(.no-ripple)');
        buttons.forEach(btn => {
            if (!btn.classList.contains('ripple')) {
                btn.classList.add('ripple', 'btn-press');
            }
        });

        // Animate counters on page load
        const counters = document.querySelectorAll('[data-count-to]');
        counters.forEach(counter => {
            const endValue = parseInt(counter.dataset.countTo);
            CounterAnimation.animateElement(counter, endValue);
        });

        // Initialize stagger animations for feature cards
        StaggerAnimation.init('.welcome-features', '.feature-card');

        console.log('[Animations] All animation systems initialized ✓');
    };

    // Make utilities globally available
    window.AnimationUtils = {
        SkeletonLoader,
        ToastManager,
        CounterAnimation,
        TypingAnimation,
        ShakeEffect,
        LoadingOverlay,
        ButtonAnimations,
        RippleEffect,
        StaggerAnimation
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initAnimations);
    } else {
        initAnimations();
    }

    // Add CSS for ripple effect
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rippleEffect {
            to {
                transform: translate(-50%, -50%) scale(40);
                opacity: 0;
            }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
    `;
    document.head.appendChild(style);

})();

/**
 * Mobile-Specific JavaScript Functionality
 * Touch gestures, mobile menu, and responsive behaviors
 */

(function() {
    'use strict';

    // ==================== MOBILE DETECTION ====================
    const isMobile = () => {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    };

    const isTablet = () => {
        return /(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(navigator.userAgent);
    };

    const isTouchDevice = () => {
        return ('ontouchstart' in window) || (navigator.maxTouchPoints > 0);
    };

    // ==================== MOBILE MENU ====================
    class MobileMenu {
        constructor() {
            this.menuButton = null;
            this.sidebar = null;
            this.overlay = null;
            this.isOpen = false;
            this.init();
        }

        init() {
            // Create mobile menu button if on mobile/tablet
            if (window.innerWidth <= 992) {
                this.createMenuButton();
                this.createOverlay();
                this.setupEventListeners();
            }

            // Handle window resize
            window.addEventListener('resize', () => {
                if (window.innerWidth > 992) {
                    this.hideMenuButton();
                    this.close();
                } else if (!this.menuButton) {
                    this.createMenuButton();
                    this.createOverlay();
                    this.setupEventListeners();
                }
            });
        }

        createMenuButton() {
            if (this.menuButton) return;

            this.menuButton = document.createElement('button');
            this.menuButton.className = 'mobile-menu-toggle';
            this.menuButton.innerHTML = '<i class="fas fa-bars"></i>';
            this.menuButton.setAttribute('aria-label', 'Toggle Menu');
            document.body.appendChild(this.menuButton);
        }

        createOverlay() {
            if (this.overlay) return;

            this.overlay = document.createElement('div');
            this.overlay.className = 'sidebar-overlay';
            document.body.appendChild(this.overlay);
        }

        setupEventListeners() {
            this.sidebar = document.querySelector('.quick-actions-panel');

            if (this.menuButton) {
                this.menuButton.addEventListener('click', () => this.toggle());
            }

            if (this.overlay) {
                this.overlay.addEventListener('click', () => this.close());
            }

            // Close on escape key
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isOpen) {
                    this.close();
                }
            });

            // Close when clicking quick action
            if (this.sidebar) {
                this.sidebar.addEventListener('click', (e) => {
                    if (e.target.classList.contains('quick-action-btn')) {
                        setTimeout(() => this.close(), 300);
                    }
                });
            }
        }

        toggle() {
            this.isOpen ? this.close() : this.open();
        }

        open() {
            if (!this.sidebar) return;
            
            this.sidebar.classList.add('active');
            this.overlay.classList.add('active');
            this.menuButton.innerHTML = '<i class="fas fa-times"></i>';
            this.isOpen = true;

            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }

        close() {
            if (!this.sidebar) return;

            this.sidebar.classList.remove('active');
            this.overlay.classList.remove('active');
            this.menuButton.innerHTML = '<i class="fas fa-bars"></i>';
            this.isOpen = false;

            // Restore body scroll
            document.body.style.overflow = '';
        }

        hideMenuButton() {
            if (this.menuButton) {
                this.menuButton.style.display = 'none';
            }
            if (this.overlay) {
                this.overlay.style.display = 'none';
            }
        }
    }

    // ==================== TOUCH GESTURES ====================
    class TouchGestures {
        constructor() {
            this.startX = 0;
            this.startY = 0;
            this.distX = 0;
            this.distY = 0;
            this.threshold = 100; // minimum swipe distance
            this.restraint = 100; // maximum perpendicular distance
            this.allowedTime = 500; // maximum swipe time
            this.startTime = 0;
            this.init();
        }

        init() {
            if (!isTouchDevice()) return;

            const messagesContainer = document.getElementById('messagesContainer');
            if (messagesContainer) {
                messagesContainer.addEventListener('touchstart', (e) => this.handleTouchStart(e), false);
                messagesContainer.addEventListener('touchmove', (e) => this.handleTouchMove(e), false);
                messagesContainer.addEventListener('touchend', (e) => this.handleTouchEnd(e), false);
            }

            // Pull to refresh gesture
            this.initPullToRefresh();
        }

        handleTouchStart(e) {
            const touch = e.changedTouches[0];
            this.startX = touch.pageX;
            this.startY = touch.pageY;
            this.startTime = new Date().getTime();
        }

        handleTouchMove(e) {
            // Prevent default only if necessary to allow native scrolling
        }

        handleTouchEnd(e) {
            const touch = e.changedTouches[0];
            this.distX = touch.pageX - this.startX;
            this.distY = touch.pageY - this.startY;
            const elapsedTime = new Date().getTime() - this.startTime;

            if (elapsedTime <= this.allowedTime) {
                // Swipe left (show menu on left swipe)
                if (Math.abs(this.distX) >= this.threshold && Math.abs(this.distY) <= this.restraint) {
                    if (this.distX > 0) {
                        // Swipe right - could open menu
                        this.handleSwipeRight();
                    } else {
                        // Swipe left - could close menu
                        this.handleSwipeLeft();
                    }
                }
            }
        }

        handleSwipeRight() {
            // Open mobile menu on swipe right
            if (window.innerWidth <= 992) {
                const menu = document.querySelector('.quick-actions-panel');
                if (menu && !menu.classList.contains('active')) {
                    // Trigger menu open
                    const menuToggle = document.querySelector('.mobile-menu-toggle');
                    if (menuToggle) menuToggle.click();
                }
            }
        }

        handleSwipeLeft() {
            // Close mobile menu on swipe left
            const menu = document.querySelector('.quick-actions-panel');
            if (menu && menu.classList.contains('active')) {
                const overlay = document.querySelector('.sidebar-overlay');
                if (overlay) overlay.click();
            }
        }

        initPullToRefresh() {
            // Optional: Add pull-to-refresh functionality
            // Implementation can be added if needed
        }
    }

    // ==================== VIEWPORT HEIGHT FIX (iOS Safari) ====================
    class ViewportFix {
        constructor() {
            this.init();
        }

        init() {
            // Fix for iOS Safari address bar height issue
            const setViewportHeight = () => {
                const vh = window.innerHeight * 0.01;
                document.documentElement.style.setProperty('--vh', `${vh}px`);
            };

            setViewportHeight();
            window.addEventListener('resize', setViewportHeight);
            window.addEventListener('orientationchange', setViewportHeight);
        }
    }

    // ==================== KEYBOARD HANDLING ====================
    class KeyboardHandler {
        constructor() {
            this.init();
        }

        init() {
            if (!isMobile()) return;

            const messageInput = document.getElementById('messageInput');
            if (!messageInput) return;

            // Scroll to input when keyboard opens
            messageInput.addEventListener('focus', () => {
                setTimeout(() => {
                    messageInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            });

            // Handle keyboard visibility
            if (window.visualViewport) {
                window.visualViewport.addEventListener('resize', () => {
                    const inputContainer = document.querySelector('.input-container');
                    if (inputContainer) {
                        const keyboardHeight = window.innerHeight - window.visualViewport.height;
                        if (keyboardHeight > 150) {
                            // Keyboard is open
                            inputContainer.style.bottom = `${keyboardHeight}px`;
                        } else {
                            // Keyboard is closed
                            inputContainer.style.bottom = '0';
                        }
                    }
                });
            }
        }
    }

    // ==================== HAPTIC FEEDBACK ====================
    class HapticFeedback {
        constructor() {
            this.canVibrate = 'vibrate' in navigator;
        }

        light() {
            if (this.canVibrate) {
                navigator.vibrate(10);
            }
        }

        medium() {
            if (this.canVibrate) {
                navigator.vibrate(20);
            }
        }

        heavy() {
            if (this.canVibrate) {
                navigator.vibrate(30);
            }
        }

        success() {
            if (this.canVibrate) {
                navigator.vibrate([10, 50, 10]);
            }
        }

        error() {
            if (this.canVibrate) {
                navigator.vibrate([50, 100, 50]);
            }
        }
    }

    // ==================== ORIENTATION HANDLER ====================
    class OrientationHandler {
        constructor() {
            this.init();
        }

        init() {
            window.addEventListener('orientationchange', () => {
                // Adjust layout on orientation change
                setTimeout(() => {
                    this.adjustLayout();
                }, 100);
            });
        }

        adjustLayout() {
            const isLandscape = window.orientation === 90 || window.orientation === -90;
            const body = document.body;

            if (isLandscape) {
                body.classList.add('landscape');
                body.classList.remove('portrait');
            } else {
                body.classList.add('portrait');
                body.classList.remove('landscape');
            }
        }
    }

    // ==================== NETWORK STATUS ====================
    class NetworkStatus {
        constructor() {
            this.init();
        }

        init() {
            window.addEventListener('online', () => this.handleOnline());
            window.addEventListener('offline', () => this.handleOffline());
        }

        handleOnline() {
            this.showToast('You are back online! 🌐', 'success');
            document.body.classList.remove('offline');
        }

        handleOffline() {
            this.showToast('No internet connection ⚠️', 'error');
            document.body.classList.add('offline');
        }

        showToast(message, type) {
            // Create toast notification
            const toast = document.createElement('div');
            toast.className = `mobile-toast mobile-toast-${type}`;
            toast.textContent = message;
            toast.style.cssText = `
                position: fixed;
                top: 80px;
                left: 50%;
                transform: translateX(-50%);
                background: ${type === 'success' ? '#10b981' : '#ef4444'};
                color: white;
                padding: 12px 24px;
                border-radius: 24px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                z-index: 10000;
                font-size: 14px;
                animation: slideDown 0.3s ease-out;
            `;

            document.body.appendChild(toast);

            setTimeout(() => {
                toast.style.animation = 'slideUp 0.3s ease-out';
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
    }

    // ==================== PERFORMANCE MONITOR ====================
    class PerformanceMonitor {
        constructor() {
            this.init();
        }

        init() {
            // Lazy load images
            if ('IntersectionObserver' in window) {
                this.lazyLoadImages();
            }

            // Reduce animations on low-end devices
            this.detectLowEndDevice();
        }

        lazyLoadImages() {
            const images = document.querySelectorAll('img[data-src]');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => observer.observe(img));
        }

        detectLowEndDevice() {
            // Check hardware concurrency (CPU cores)
            const cores = navigator.hardwareConcurrency || 2;
            // Check memory (if available)
            const memory = navigator.deviceMemory || 4;

            if (cores <= 2 || memory <= 2) {
                document.body.classList.add('low-end-device');
                // Disable heavy animations
                const style = document.createElement('style');
                style.textContent = `
                    .low-end-device * {
                        animation-duration: 0.2s !important;
                        transition-duration: 0.2s !important;
                    }
                `;
                document.head.appendChild(style);
            }
        }
    }

    // ==================== INITIALIZE ALL MOBILE FEATURES ====================
    const initMobileFeatures = () => {
        // Initialize all mobile-specific features
        new MobileMenu();
        new TouchGestures();
        new ViewportFix();
        new KeyboardHandler();
        new OrientationHandler();
        new NetworkStatus();
        new PerformanceMonitor();

        // Make haptic feedback globally available
        window.hapticFeedback = new HapticFeedback();

        // Add touch-device class to body
        if (isTouchDevice()) {
            document.body.classList.add('touch-device');
        }

        if (isMobile()) {
            document.body.classList.add('mobile-device');
        }

        if (isTablet()) {
            document.body.classList.add('tablet-device');
        }

        console.log('[Mobile] All mobile features initialized ✓');
    };

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMobileFeatures);
    } else {
        initMobileFeatures();
    }

    // Export for global access
    window.MobileUtils = {
        isMobile,
        isTablet,
        isTouchDevice
    };

})();

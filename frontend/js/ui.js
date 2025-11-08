/* ============================================
   VHU CHATBOT - UI CONTROLS
   Created by: Hải - VHU Student
   Version: 1.0
   ============================================ */

// ==================== CHAT WIDGET CONTROLS ====================

/**
 * Toggle chat widget visibility
 */
function toggleChat() {
    const widget = document.getElementById('chatWidget');
    const button = document.getElementById('chatButton');
    
    if (widget.classList.contains('hidden')) {
        openChat();
    } else {
        closeChat();
    }
}

/**
 * Open chat widget
 */
function openChat() {
    const widget = document.getElementById('chatWidget');
    const button = document.getElementById('chatButton');
    
    widget.classList.remove('hidden');
    button.classList.add('hidden');
    
    // Focus on input field
    const inputField = document.getElementById('userInput');
    if (inputField) {
        inputField.focus();
    }
    
    // Show welcome message if chat is empty
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer && messagesContainer.children.length === 0) {
        if (CHATBOT_SETTINGS.autoGreeting) {
            setTimeout(() => {
                displayWelcomeMessage();
            }, CHATBOT_SETTINGS.greetingDelay);
        }
    }
    
    scrollToBottom();
    debugLog('Chat opened');
}

/**
 * Close chat widget
 */
function closeChat() {
    const widget = document.getElementById('chatWidget');
    const button = document.getElementById('chatButton');
    
    widget.classList.add('hidden');
    button.classList.remove('hidden');
    
    debugLog('Chat closed');
}

/**
 * Minimize chat (same as close for now)
 */
function minimizeChat() {
    closeChat();
}

// ==================== UI HELPERS ====================

/**
 * Scroll messages container to bottom smoothly
 */
function scrollToBottom() {
    setTimeout(() => {
        const messagesContainer = document.getElementById('messagesContainer');
        if (messagesContainer) {
            messagesContainer.scrollTo({
                top: messagesContainer.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, CONSTANTS.SCROLL_DELAY);
}

/**
 * Update chat header status
 */
function updateChatStatus(status, color = 'green') {
    const statusDot = document.querySelector('.status-dot');
    if (statusDot) {
        statusDot.className = `status-dot w-2 h-2 bg-${color}-400 rounded-full`;
    }
}

/**
 * Show loading state
 */
function showLoading() {
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.innerHTML = '<div class="loading-spinner"></div>';
    }
}

/**
 * Hide loading state
 */
function hideLoading() {
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.disabled = false;
        sendButton.innerHTML = '<i class="fas fa-paper-plane"></i>';
    }
}

/**
 * Disable input while waiting for response
 */
function disableInput() {
    const inputField = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    if (inputField) inputField.disabled = true;
    if (sendButton) sendButton.disabled = true;
}

/**
 * Enable input after receiving response
 */
function enableInput() {
    const inputField = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');
    
    if (inputField) {
        inputField.disabled = false;
        inputField.focus();
    }
    if (sendButton) sendButton.disabled = false;
}

// ==================== NOTIFICATION SYSTEM ====================

/**
 * Show custom notification
 */
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    
    const colors = {
        success: 'bg-green-500',
        error: 'bg-red-500',
        warning: 'bg-yellow-500',
        info: 'bg-blue-500'
    };
    
    const icons = {
        success: '✓',
        error: '✗',
        warning: '⚠',
        info: 'ℹ'
    };
    
    notification.className = `notification fixed top-4 right-4 ${colors[type]} text-white px-6 py-3 rounded-lg shadow-lg z-50 flex items-center gap-2`;
    notification.innerHTML = `
        <span class="text-xl font-bold">${icons[type]}</span>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// ==================== MODAL SYSTEM ====================

/**
 * Show modal dialog
 */
function showModal(title, content, buttons = []) {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center';
    overlay.id = 'modalOverlay';
    
    // Create modal content
    const modal = document.createElement('div');
    modal.className = 'bg-white rounded-xl shadow-2xl max-w-md w-full mx-4 overflow-hidden';
    modal.innerHTML = `
        <div class="bg-gradient-to-r from-vhu-blue to-blue-700 px-6 py-4">
            <h3 class="text-xl font-bold text-white">${title}</h3>
        </div>
        <div class="p-6">
            <div class="text-gray-700 mb-6">${content}</div>
            <div class="flex gap-3 justify-end" id="modalButtons"></div>
        </div>
    `;
    
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Add buttons
    const buttonContainer = modal.querySelector('#modalButtons');
    buttons.forEach(btn => {
        const button = document.createElement('button');
        button.className = `px-4 py-2 rounded-lg font-medium transition-all ${btn.primary ? 'bg-vhu-blue text-white hover:bg-blue-700' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`;
        button.textContent = btn.text;
        button.onclick = () => {
            if (btn.onClick) btn.onClick();
            closeModal();
        };
        buttonContainer.appendChild(button);
    });
    
    // Close on overlay click
    overlay.onclick = (e) => {
        if (e.target === overlay) closeModal();
    };
}

/**
 * Close modal dialog
 */
function closeModal() {
    const overlay = document.getElementById('modalOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// ==================== CHAT STATISTICS ====================

/**
 * Get chat statistics
 */
function getChatStatistics() {
    const totalMessages = messageHistory.length;
    const userMessages = messageHistory.filter(m => m.sender === 'user').length;
    const botMessages = messageHistory.filter(m => m.sender === 'bot').length;
    
    return {
        total: totalMessages,
        user: userMessages,
        bot: botMessages,
        startTime: messageHistory[0]?.timestamp || null,
        endTime: messageHistory[messageHistory.length - 1]?.timestamp || null
    };
}

/**
 * Show chat statistics modal
 */
function showStatistics() {
    const stats = getChatStatistics();
    
    const content = `
        <div class="space-y-3">
            <div class="flex justify-between">
                <span class="font-medium">Tổng tin nhắn:</span>
                <span class="text-vhu-blue font-bold">${stats.total}</span>
            </div>
            <div class="flex justify-between">
                <span class="font-medium">Tin của bạn:</span>
                <span class="text-vhu-blue font-bold">${stats.user}</span>
            </div>
            <div class="flex justify-between">
                <span class="font-medium">Tin của bot:</span>
                <span class="text-vhu-blue font-bold">${stats.bot}</span>
            </div>
            <div class="border-t pt-3 mt-3">
                <div class="text-sm text-gray-500">Session ID: ${getUserId()}</div>
            </div>
        </div>
    `;
    
    showModal('📊 Thống kê cuộc trò chuyện', content, [
        { text: 'Đóng', primary: false }
    ]);
}

// ==================== KEYBOARD SHORTCUTS ====================

/**
 * Handle keyboard shortcuts
 */
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + K: Open/Close chat
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        toggleChat();
    }
    
    // Ctrl/Cmd + L: Clear chat
    if ((event.ctrlKey || event.metaKey) && event.key === 'l') {
        event.preventDefault();
        clearChat();
    }
    
    // Escape: Close chat
    if (event.key === 'Escape') {
        const widget = document.getElementById('chatWidget');
        if (widget && !widget.classList.contains('hidden')) {
            closeChat();
        }
    }
}

// ==================== RESPONSIVE HANDLING ====================

/**
 * Handle window resize
 */
function handleResize() {
    const widget = document.getElementById('chatWidget');
    
    if (window.innerWidth < 768) {
        // Mobile: Full screen chat
        if (widget) {
            widget.style.width = '100%';
            widget.style.height = '100%';
            widget.style.bottom = '0';
            widget.style.right = '0';
            widget.style.borderRadius = '0';
        }
    } else {
        // Desktop: Normal size
        if (widget) {
            widget.style.width = CHATBOT_SETTINGS.chatWindowWidth;
            widget.style.height = CHATBOT_SETTINGS.chatWindowHeight;
            widget.style.bottom = '1.5rem';
            widget.style.right = '1.5rem';
            widget.style.borderRadius = '1rem';
        }
    }
}

// ==================== ACCESSIBILITY ====================

/**
 * Announce message to screen readers
 */
function announceMessage(message) {
    const announcement = document.createElement('div');
    announcement.className = 'sr-only';
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.textContent = message;
    
    document.body.appendChild(announcement);
    
    setTimeout(() => announcement.remove(), 1000);
}

// ==================== THEME TOGGLE (Future Feature) ====================

/**
 * Toggle dark mode (placeholder for future)
 */
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('vhu-chatbot-theme', isDark ? 'dark' : 'light');
}

/**
 * Load saved theme
 */
function loadTheme() {
    const savedTheme = localStorage.getItem('vhu-chatbot-theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
    }
}

// ==================== INITIALIZATION ====================

/**
 * Initialize UI controls
 */
function initializeUI() {
    debugLog('Initializing UI controls...');
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', handleKeyboardShortcuts);
    
    // Handle window resize
    window.addEventListener('resize', handleResize);
    handleResize(); // Initial call
    
    // Load theme
    loadTheme();
    
    // Update status indicator
    updateChatStatus('online', 'green');
    
    debugLog('UI controls initialized');
}

// ==================== EXPORT ====================

window.toggleChat = toggleChat;
window.openChat = openChat;
window.closeChat = closeChat;
window.minimizeChat = minimizeChat;
window.scrollToBottom = scrollToBottom;
window.updateChatStatus = updateChatStatus;
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.disableInput = disableInput;
window.enableInput = enableInput;
window.showNotification = showNotification;
window.showModal = showModal;
window.closeModal = closeModal;
window.showStatistics = showStatistics;
window.toggleDarkMode = toggleDarkMode;
window.initializeUI = initializeUI;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUI);
} else {
    initializeUI();
}

console.log('✅ VHU Chatbot UI Controls loaded successfully');

/* ============================================
   VHU CHATBOT - CHAT LOGIC
   Created by: Hải - VHU Student
   Version: 1.0
   ============================================ */

// ==================== GLOBAL STATE ====================

let isWaitingForResponse = false;
let messageHistory = [];

// ==================== SEND MESSAGE TO RASA ====================

/**
 * Send user message to Rasa and display responses
 */
async function sendMessage(message = null) {
    // Get message from input if not provided
    if (!message) {
        const inputField = document.getElementById('userInput');
        message = inputField.value.trim();
        inputField.value = '';
    }
    
    // Validate message
    const validation = validateMessage(message);
    if (!validation.valid) {
        showErrorNotification(validation.error);
        return;
    }
    
    // Prevent multiple simultaneous requests
    if (isWaitingForResponse) {
        showErrorNotification('Vui lòng đợi phản hồi trước đó!');
        return;
    }
    
    debugLog('Sending message:', message);
    
    // Display user message
    displayUserMessage(message);
    
    // Add to history
    messageHistory.push({
        sender: 'user',
        text: message,
        timestamp: new Date()
    });
    
    // Show typing indicator
    showTypingIndicator();
    isWaitingForResponse = true;
    
    try {
        // Call Rasa API
        const response = await fetch(CONFIG.RASA_API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sender: getUserId(),
                message: message
            }),
            signal: AbortSignal.timeout(CONFIG.API_TIMEOUT)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        debugLog('Received response:', data);
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Process and display bot responses
        if (data && data.length > 0) {
            for (let i = 0; i < data.length; i++) {
                await displayBotResponse(data[i], i);
            }
        } else {
            // No response from bot
            displayBotMessage('Xin lỗi, tôi không hiểu câu hỏi của bạn. Bạn có thể hỏi lại được không?');
        }
        
    } catch (error) {
        debugLog('Error sending message:', error);
        hideTypingIndicator();
        
        // Display appropriate error message
        if (error.name === 'AbortError' || error.name === 'TimeoutError') {
            displayBotMessage(CONSTANTS.ERRORS.TIMEOUT);
        } else if (error.message.includes('Failed to fetch')) {
            displayBotMessage(CONSTANTS.ERRORS.CONNECTION);
        } else {
            displayBotMessage(CONSTANTS.ERRORS.UNKNOWN);
        }
    } finally {
        isWaitingForResponse = false;
    }
}

// ==================== DISPLAY MESSAGES ====================

/**
 * Display user message in chat
 */
function displayUserMessage(text) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex justify-end mb-4 animate-fadeIn';
    
    const bubble = document.createElement('div');
    bubble.className = 'user-message bg-gradient-to-r from-vhu-blue to-blue-600 text-white rounded-2xl rounded-tr-sm px-5 py-3 shadow-md max-w-md';
    bubble.textContent = text;
    
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

/**
 * Format Markdown text to HTML
 */
function formatMarkdown(text) {
    // Escape HTML first
    let formatted = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Convert Markdown to HTML
    // Bold: **text** or __text__
    formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong class="font-bold text-vhu-blue">$1</strong>');
    formatted = formatted.replace(/__(.+?)__/g, '<strong class="font-bold text-vhu-blue">$1</strong>');
    
    // Italic: *text* or _text_
    formatted = formatted.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>');
    formatted = formatted.replace(/_(.+?)_/g, '<em class="italic">$1</em>');
      // Detect and add icons for common content types
    // Ngành học / Programs
    if (text.match(/ngành|chương trình đào tạo|đào tạo/i)) {
        formatted = '📚 ' + formatted;
    }
    // Học phí / Tuition
    else if (text.match(/học phí|chi phí|tiền học|VNĐ|vnđ/i)) {
        formatted = '💰 ' + formatted;
    }
    // Học bổng / Scholarship
    else if (text.match(/học bổng|hỗ trợ|miễn giảm/i)) {
        formatted = '🏅 ' + formatted;
    }
    // Địa chỉ / Location
    else if (text.match(/địa chỉ|cơ sở|quận|đường|hướng dẫn đi/i)) {
        formatted = '📍 ' + formatted;
    }
    // Liên hệ / Contact
    else if (text.match(/liên hệ|hotline|email|phone|điện thoại/i)) {
        formatted = '📞 ' + formatted;
    }
    // Tuyển sinh / Admission
    else if (text.match(/tuyển sinh|xét tuyển|nhập học|hồ sơ/i)) {
        formatted = '🎓 ' + formatted;
    }
    
    // Bullet points: - item or • item (with icons)
    formatted = formatted.replace(/^[\-•]\s+(Tra cứu|tra cứu)(.+)$/gmi, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">📚</span><span>Tra cứu$2</span></div>');
    formatted = formatted.replace(/^[\-•]\s+(Tính|tính)(.+)(học phí|chi phí)(.+)$/gmi, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">💰</span><span>Tính$2$3$4</span></div>');
    formatted = formatted.replace(/^[\-•]\s+(Gợi ý|gợi ý|Tư vấn|tư vấn)(.+)$/gmi, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">🎯</span><span>$1$2</span></div>');
    formatted = formatted.replace(/^[\-•]\s+(Chỉ đường|chỉ đường)(.+)$/gmi, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">🗺️</span><span>Chỉ đường$2</span></div>');
    formatted = formatted.replace(/^[\-•]\s+(Tra cứu học bổng|học bổng)(.+)$/gmi, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">🏅</span><span>$1$2</span></div>');
    formatted = formatted.replace(/^[\-•]\s+(.+)$/gm, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue mr-2">•</span><span>$1</span></div>');
    
    // Numbered lists: 1. item
    formatted = formatted.replace(/^(\d+)\.\s+(.+)$/gm, '<div class="flex items-start ml-2 my-1.5"><span class="text-vhu-blue font-bold mr-2">$1.</span><span>$2</span></div>');
    
    // Headers: ## Header
    formatted = formatted.replace(/^###\s+(.+)$/gm, '<h4 class="text-sm font-bold text-gray-700 mt-2 mb-1">$1</h4>');
    formatted = formatted.replace(/^##\s+(.+)$/gm, '<h3 class="text-base font-bold text-vhu-blue mt-2 mb-1">$1</h3>');
    formatted = formatted.replace(/^#\s+(.+)$/gm, '<h2 class="text-lg font-bold text-vhu-blue mt-2 mb-1">$1</h2>');
    
    // Links: [text](url)
    formatted = formatted.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank" class="text-blue-500 hover:underline">$1</a>');
    
    // Emoji icons at start of line (expand list)
    formatted = formatted.replace(/^(📚|💰|🎓|📍|🏅|📞|📧|🌐|✅|❌|⚠️|ℹ️|🎯|📊|🗺️|🔍|💡|⭐)\s+/gm, '<span class="text-xl mr-2 inline-block">$1</span>');
    
    // Line breaks - FIX: Remove excessive spacing
    formatted = formatted.replace(/\n\n+/g, '<br>'); // Multiple newlines → single <br>
    formatted = formatted.replace(/\n/g, '<br>');
    
    return formatted;
}

/**
 * Display bot message in chat
 */
function displayBotMessage(text, buttons = null) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex justify-start mb-4 animate-fadeIn';
    
    // Add VHU logo avatar
    const avatar = document.createElement('div');
    avatar.className = 'w-8 h-8 bg-white rounded-full flex items-center justify-center overflow-hidden border-2 border-vhu-blue mr-2 flex-shrink-0';
    
    const logoImg = document.createElement('img');
    logoImg.src = 'assets/image/logo-vhu.jpg';
    logoImg.alt = 'VHU Bot';
    logoImg.className = 'w-full h-full object-cover';
    avatar.appendChild(logoImg);
    
    const bubble = document.createElement('div');
    bubble.className = 'bot-message bg-white text-gray-800 rounded-2xl rounded-tl-sm px-5 py-3 shadow-md max-w-md';
    
    // Format markdown and display
    bubble.innerHTML = formatMarkdown(text);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    messagesContainer.appendChild(messageDiv);
    
    // Add buttons if provided
    if (buttons && buttons.length > 0) {
        displayQuickReplies(buttons);
    }
    
    // Add to history
    messageHistory.push({
        sender: 'bot',
        text: text,
        timestamp: new Date()
    });
    
    scrollToBottom();
}

/**
 * Process and display bot response (handles multiple response types)
 */
async function displayBotResponse(response, index = 0) {
    // Add delay between multiple responses
    if (index > 0) {
        await delay(500);
    }
    
    // Handle text response
    if (response.text) {
        displayBotMessage(response.text);
    }
    
    // Handle image response
    if (response.image) {
        displayImageMessage(response.image);
    }
    
    // Handle custom response (for maps, forms, etc.)
    if (response.custom) {
        handleCustomResponse(response.custom);
    }
    
    // Handle buttons/quick replies
    if (response.buttons && response.buttons.length > 0) {
        displayQuickReplies(response.buttons);
    }
}

/**
 * Display quick reply buttons
 */
function displayQuickReplies(buttons) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const quickRepliesDiv = document.createElement('div');
    quickRepliesDiv.className = 'flex flex-wrap gap-2 mb-4 ml-4';
    
    buttons.forEach(button => {
        const btn = document.createElement('button');
        btn.className = 'quick-reply-btn bg-white text-vhu-blue px-4 py-2 rounded-full text-sm font-medium hover:bg-vhu-blue hover:text-white transition-all';
        btn.textContent = button.title || button.payload;
        
        btn.onclick = () => {
            const message = button.payload || button.title;
            sendMessage(message);
            // Remove quick replies after clicking
            quickRepliesDiv.remove();
        };
        
        quickRepliesDiv.appendChild(btn);
    });
    
    messagesContainer.appendChild(quickRepliesDiv);
    scrollToBottom();
}

/**
 * Display image message
 */
function displayImageMessage(imageUrl) {
    const messagesContainer = document.getElementById('messagesContainer');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'flex justify-start mb-4';
    
    const img = document.createElement('img');
    img.src = imageUrl;
    img.className = 'rounded-lg max-w-xs shadow-lg';
    img.alt = 'Image from bot';
    
    messageDiv.appendChild(img);
    messagesContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

/**
 * Handle custom response types (maps, forms, etc.)
 */
function handleCustomResponse(customData) {
    debugLog('Custom response:', customData);
    
    // Handle GPS/Maps response
    if (customData.type === 'map' || customData.google_maps_url) {
        const mapUrl = customData.google_maps_url || customData.url;
        displayBotMessage(`📍 Bạn có thể xem chỉ đường tại đây: ${mapUrl}`);
    }
    
    // Handle other custom types as needed
    // Future: Display interactive forms, cards, etc.
}

// ==================== TYPING INDICATOR ====================

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.remove('hidden');
        scrollToBottom();
    }
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.classList.add('hidden');
    }
}

// ==================== CHAT CONTROLS ====================

/**
 * Clear chat history
 */
function clearChat() {
    if (!confirm('Bạn có chắc muốn xóa toàn bộ cuộc trò chuyện?')) {
        return;
    }
    
    const messagesContainer = document.getElementById('messagesContainer');
    messagesContainer.innerHTML = '';
    
    messageHistory = [];
    
    // Show welcome message again
    setTimeout(() => {
        displayWelcomeMessage();
    }, 300);
    
    debugLog('Chat cleared');
}

/**
 * Display welcome message
 */
function displayWelcomeMessage() {
    displayBotMessage(CONSTANTS.WELCOME_MESSAGE);
    
    // Show initial quick replies
    if (CONFIG.FEATURES.quickReplies) {
        const quickReplyButtons = CONSTANTS.QUICK_REPLIES.map(text => ({
            title: text,
            payload: text
        }));
        displayQuickReplies(quickReplyButtons);
    }
}

/**
 * Handle Enter key press in input field
 */
function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

/**
 * Export chat history (for debugging or saving)
 */
function exportChatHistory() {
    const dataStr = JSON.stringify(messageHistory, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = `vhu-chat-history-${Date.now()}.json`;
    link.click();
    
    URL.revokeObjectURL(url);
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Scroll messages container to bottom
 */
function scrollToBottom() {
    setTimeout(() => {
        const messagesContainer = document.getElementById('messagesContainer');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }, CONSTANTS.SCROLL_DELAY);
}

/**
 * Delay helper function
 */
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Show error notification
 */
function showErrorNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'notification notification-error fixed top-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Show success notification
 */
function showSuccessNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification notification-success fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50';
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ==================== INITIALIZATION ====================

/**
 * Initialize chat when page loads
 */
function initializeChat() {
    debugLog('Initializing chat...');
    
    // Check server health
    checkServerHealth().then(isHealthy => {
        if (isHealthy) {
            debugLog('✅ Rasa server is running');
        } else {
            console.warn('⚠️ Rasa server may not be running on port 5005');
        }
    });
    
    // Add event listener for Enter key
    const inputField = document.getElementById('userInput');
    if (inputField) {
        inputField.addEventListener('keypress', handleKeyPress);
    }
    
    debugLog('Chat initialized successfully');
}

// ==================== EXPORT ====================

window.sendMessage = sendMessage;
window.clearChat = clearChat;
window.displayWelcomeMessage = displayWelcomeMessage;
window.handleKeyPress = handleKeyPress;
window.exportChatHistory = exportChatHistory;
window.initializeChat = initializeChat;

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChat);
} else {
    initializeChat();
}

console.log('✅ VHU Chatbot Chat Logic loaded successfully');

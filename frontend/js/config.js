/* ============================================
   VHU CHATBOT - CONFIGURATION
   Created by: Hải - VHU Student
   Version: 1.0
   ============================================ */

// ==================== API CONFIGURATION ====================

const CONFIG = {
    // Rasa REST API Endpoint
    RASA_API_URL: 'http://localhost:5005/webhooks/rest/webhook',
    
    // API Timeout (milliseconds)
    API_TIMEOUT: 10000,
    
    // Rasa Action Server URL (for debugging)
    ACTION_SERVER_URL: 'http://localhost:5055',
    
    // Enable/Disable features
    FEATURES: {
        quickReplies: true,
        typing_indicator: true,
        clearChat: true,
        timestamps: true
    }
};

// ==================== USER CONFIGURATION ====================

// Generate unique user ID for this session
function generateUserId() {
    const timestamp = Date.now();
    const random = Math.floor(Math.random() * 10000);
    return `user_${timestamp}_${random}`;
}

// Get or create user ID (persists in sessionStorage)
function getUserId() {
    let userId = sessionStorage.getItem('vhu_chatbot_user_id');
    if (!userId) {
        userId = generateUserId();
        sessionStorage.setItem('vhu_chatbot_user_id', userId);
    }
    return userId;
}

// ==================== CONSTANTS ====================

const CONSTANTS = {
    // Maximum message length
    MAX_MESSAGE_LENGTH: 500,
    
    // Typing indicator delay (milliseconds)
    TYPING_DELAY: 1000,
    
    // Auto-scroll delay
    SCROLL_DELAY: 100,
      // Welcome message (shown when chat opens)
    WELCOME_MESSAGE: 'Xin chào! Tôi là VHU Assistant 🎓\nTôi có thể giúp bạn:\n- Tra cứu 44 ngành đào tạo\n- Tính học phí chi tiết\n- Gợi ý ngành phù hợp\n- Chỉ đường đến các cơ sở\n- Tra cứu học bổng\nBạn muốn tìm hiểu về điều gì?',
    
    // Error messages
    ERRORS: {
        CONNECTION: '❌ Không thể kết nối đến server. Vui lòng kiểm tra:\n1. Rasa server đang chạy (port 5005)\n2. Action server đang chạy (port 5055)\n3. CORS đã được cấu hình',
        TIMEOUT: '⏱️ Yêu cầu timeout. Server phản hồi quá lâu.',
        EMPTY_MESSAGE: 'Vui lòng nhập tin nhắn!',
        TOO_LONG: `Tin nhắn quá dài! Tối đa ${500} ký tự.`,
        UNKNOWN: '❌ Có lỗi xảy ra. Vui lòng thử lại.'
    },
    
    // Quick reply suggestions (shown at start)
    QUICK_REPLIES: [
        '44 ngành đào tạo',
        'Tính học phí',
        'Gợi ý ngành học',
        'Chỉ đường đến VHU',
        'Học bổng'
    ],
    
    // VHU Information
    VHU_INFO: {
        fullName: 'Đại học Văn Hiến',
        shortName: 'VHU',
        website: 'https://vhu.edu.vn',
        phone: '028.7309.8989',
        email: 'tuyensinh@vhu.edu.vn',
        address: '665-667-669 Điện Biên Phủ, P.1, Q.3, TP.HCM'
    }
};

// ==================== CHATBOT SETTINGS ====================

const CHATBOT_SETTINGS = {
    // UI Settings
    chatWindowWidth: '400px',
    chatWindowHeight: '600px',
    
    // Message Settings
    maxMessagesDisplay: 100, // Clear old messages if exceeded
    
    // Animation Settings
    messageAnimationDuration: 300, // milliseconds
    
    // Auto-responses
    autoGreeting: true,
    greetingDelay: 500, // milliseconds after opening chat
    
    // Sound effects (future feature)
    soundEnabled: false,
    
    // Debug mode
    debugMode: false
};

// ==================== HELPER FUNCTIONS ====================

/**
 * Log debug messages (only if debug mode is enabled)
 */
function debugLog(message, data = null) {
    if (CHATBOT_SETTINGS.debugMode) {
        console.log(`[VHU Chatbot Debug] ${message}`, data || '');
    }
}

/**
 * Validate message before sending
 */
function validateMessage(message) {
    if (!message || message.trim().length === 0) {
        return { valid: false, error: CONSTANTS.ERRORS.EMPTY_MESSAGE };
    }
    
    if (message.length > CONSTANTS.MAX_MESSAGE_LENGTH) {
        return { valid: false, error: CONSTANTS.ERRORS.TOO_LONG };
    }
    
    return { valid: true };
}

/**
 * Format timestamp
 */
function formatTimestamp(date = new Date()) {
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

/**
 * Sanitize HTML to prevent XSS
 */
function sanitizeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Check if Rasa server is running
 */
async function checkServerHealth() {
    try {
        const response = await fetch('http://localhost:5005/', {
            method: 'GET',
            signal: AbortSignal.timeout(3000)
        });
        return response.ok;
    } catch (error) {
        return false;
    }
}

/**
 * Get current session info
 */
function getSessionInfo() {
    return {
        userId: getUserId(),
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        language: navigator.language
    };
}

// ==================== EXPORT ====================

// Make available globally
window.CONFIG = CONFIG;
window.CONSTANTS = CONSTANTS;
window.CHATBOT_SETTINGS = CHATBOT_SETTINGS;
window.getUserId = getUserId;
window.debugLog = debugLog;
window.validateMessage = validateMessage;
window.formatTimestamp = formatTimestamp;
window.sanitizeHTML = sanitizeHTML;
window.checkServerHealth = checkServerHealth;
window.getSessionInfo = getSessionInfo;

// Log initialization
console.log('✅ VHU Chatbot Config loaded successfully');
console.log('📝 User ID:', getUserId());

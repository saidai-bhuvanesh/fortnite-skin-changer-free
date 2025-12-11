// Ultra-Premium 3D Holographic UI - Enhanced Script

// Initialize particle system
function createParticles() {
    const particleContainer = document.getElementById('particles');
    if (!particleContainer) return;

    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 10) + 's';
        particleContainer.appendChild(particle);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    initializeChat();
});

// Rest of the existing script.js code...
const API_URL = 'http://localhost:8000';
let isProcessing = false;

// DOM Elements
const messagesContainer = document.getElementById('messages');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const statusText = document.getElementById('status-text');
const charCount = document.getElementById('char-count');
const welcomeTime = document.getElementById('welcome-time');

// Initialize
function initializeChat() {
    checkBackendStatus();
    setupEventListeners();
    setWelcomeTime();
}

// Set welcome message time
function setWelcomeTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    if (welcomeTime) {
        welcomeTime.textContent = timeString;
    }
}

// Check backend status
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_URL}/`);
        if (response.ok) {
            updateStatus('Online', true);
        } else {
            updateStatus('Backend Offline', false);
        }
    } catch (error) {
        updateStatus('Backend Offline', false);
    }
}

// Update status indicator
function updateStatus(text, isOnline) {
    if (statusText) {
        statusText.textContent = text;
        const statusDot = document.querySelector('.status-dot');
        if (statusDot) {
            statusDot.style.background = isOnline ? 'var(--cyan-glow)' : '#ff4444';
        }
    }
}

// Setup event listeners
function setupEventListeners() {
    if (sendButton) {
        sendButton.addEventListener('click', handleSend);
    }

    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });

        messageInput.addEventListener('input', updateCharCount);
    }

    // Quick action buttons
    const quickActions = document.querySelectorAll('.quick-action');
    quickActions.forEach(button => {
        button.addEventListener('click', () => {
            const query = button.getAttribute('data-query');
            if (query && messageInput) {
                messageInput.value = query;
                handleSend();
            }
        });
    });

    // Auto-resize textarea
    if (messageInput) {
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = messageInput.scrollHeight + 'px';
        });
    }
}

// Update character count
function updateCharCount() {
    if (charCount && messageInput) {
        charCount.textContent = messageInput.value.length;
    }
}

// Handle send message
async function handleSend() {
    if (!messageInput || isProcessing) return;

    const message = messageInput.value.trim();
    if (!message) return;

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    updateCharCount();

    // Add user message
    addMessage(message, 'user');

    // Show typing indicator
    showTyping(true);
    isProcessing = true;

    if (sendButton) {
        sendButton.disabled = true;
    }

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Hide typing indicator
        showTyping(false);

        // Add assistant message
        addMessage(data.answer, 'assistant');

    } catch (error) {
        console.error('Error:', error);
        showTyping(false);
        addMessage('Sorry, I encountered an error. Please check if the backend is running.', 'assistant', true);
    } finally {
        isProcessing = false;
        if (sendButton) {
            sendButton.disabled = false;
        }
    }
}

// Add message to chat
function addMessage(text, sender, isError = false) {
    if (!messagesContainer) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';

    const content = document.createElement('div');
    content.className = 'message-content';

    const header = document.createElement('div');
    header.className = 'message-header';

    const author = document.createElement('span');
    author.className = 'message-author';
    author.textContent = sender === 'user' ? 'You' : 'Bhuvi AI Assistant';

    const time = document.createElement('span');
    time.className = 'message-time';
    const now = new Date();
    time.textContent = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });

    header.appendChild(author);
    header.appendChild(time);

    const messageText = document.createElement('div');
    messageText.className = 'message-text';

    if (isError) {
        messageText.innerHTML = `<p style="color: #ff4444;">⚠️ ${text}</p>`;
    } else {
        messageText.innerHTML = formatMessage(text);
    }

    content.appendChild(header);
    content.appendChild(messageText);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Format message text
function formatMessage(text) {
    // Convert markdown-style formatting
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    text = text.replace(/\n/g, '<br>');
    return text;
}

// Show/hide typing indicator
function showTyping(show) {
    if (typingIndicator) {
        typingIndicator.style.display = show ? 'flex' : 'none';
        if (show && messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
}

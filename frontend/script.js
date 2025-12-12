// Ultra-Premium 3D Holographic UI - Enhanced Script

// Initialize particle system - Enhanced
function createParticles() {
    const particleContainer = document.getElementById('particles');
    if (!particleContainer) return;

    const particleCount = 100; // Increased for denser effect

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 15 + 's';
        particle.style.animationDuration = (10 + Math.random() * 10) + 's';

        // Add size variation
        const size = 2 + Math.random() * 3;
        particle.style.width = size + 'px';
        particle.style.height = size + 'px';

        particleContainer.appendChild(particle);
    }
}

// Create Matrix Code Rain Effect
function createMatrixRain() {
    const matrixContainer = document.getElementById('matrix-rain');
    if (!matrixContainer) return;

    const characters = 'ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ01';
    const columnCount = Math.floor(window.innerWidth / 20);

    for (let i = 0; i < columnCount; i++) {
        const column = document.createElement('div');
        column.className = 'matrix-column';
        column.style.left = `${i * 20}px`;
        column.style.animationDuration = `${Math.random() * 10 + 10}s`;
        column.style.animationDelay = `${Math.random() * 5}s`;

        let text = '';
        const length = Math.floor(Math.random() * 20) + 10;
        for (let j = 0; j < length; j++) {
            text += characters.charAt(Math.floor(Math.random() * characters.length)) + '\n';
        }
        column.textContent = text;
        matrixContainer.appendChild(column);
    }
}

// Part C: Robot Parallax Effect
document.addEventListener("mousemove", (e) => {
    const robotContainer = document.querySelector('.robot-container');
    if (robotContainer) {
        // Reduced movement factor for subtler effect
        const moveX = (e.clientX - window.innerWidth / 2) * 0.005;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.005;
        // Only Apply Translate. Scale is handled by CSS animation on the child img.
        robotContainer.style.transform = `translate(${moveX}px, ${moveY}px)`;
    }
});

// ========================================
// AI TOOLBOX PANEL FUNCTIONS
// ========================================

// Toggle Toolbox Panel
function toggleToolbox() {
    const toolbox = document.getElementById('aiToolbox');
    toolbox.classList.toggle('open');
}

// Select Tool
let currentTool = null;

function selectTool(toolName) {
    // Remove active class from all tools
    document.querySelectorAll('.tool-item').forEach(item => {
        item.classList.remove('active');
    });

    // Add active class to selected tool
    event.currentTarget.classList.add('active');
    currentTool = toolName;

    // Update chat placeholder based on tool
    const input = document.getElementById('message-input');
    const toolMessages = {
        document: 'Upload or describe a document to analyze...',
        email: 'Paste email content to summarize...',
        resume: 'Upload or paste resume content...',
        project: 'Describe your project for analysis...',
        linkedin: 'What type of LinkedIn content do you need?',
        brain: 'Ask me anything from your personal knowledge base...'
    };

    if (input) {
        input.placeholder = toolMessages[toolName] || 'Ask me anything... (General Chat)';
    }

    // Show notification
    showToolNotification(toolName);
}

// Show Tool Selection Notification
function showToolNotification(toolName) {
    const toolNames = {
        document: 'Document Analyzer',
        email: 'Email Summarizer',
        resume: 'Resume Scanner',
        project: 'Project Analyzer',
        linkedin: 'LinkedIn Generator',
        brain: 'Personal Brain'
    };

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'tool-notification';
    notification.textContent = `✓ ${toolNames[toolName]} activated`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, rgba(0, 247, 255, 0.9), rgba(160, 102, 255, 0.9));
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-weight: 600;
        z-index: 200;
        animation: slideDown 0.5s ease, fadeOut 0.5s ease 2.5s;
        box-shadow: 0 4px 20px rgba(0, 247, 255, 0.5);
    `;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Add notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
        }
    }
    
    @keyframes fadeOut {
        to {
            opacity: 0;
            transform: translateX(-50%) translateY(-20px);
        }
    }
`;
document.head.appendChild(style);

// Create Binary Code Rain Effect
function createBinaryRain() {
    const binaryContainer = document.getElementById('binary-rain');
    if (!binaryContainer) return;

    const columnCount = Math.floor(window.innerWidth / 25);

    for (let i = 0; i < columnCount; i++) {
        const column = document.createElement('div');
        column.className = 'binary-column';
        column.style.left = `${i * 25}px`;
        column.style.animationDuration = `${Math.random() * 8 + 8}s`;
        column.style.animationDelay = `${Math.random() * 4}s`;

        let text = '';
        const length = Math.floor(Math.random() * 15) + 8;
        for (let j = 0; j < length; j++) {
            text += (Math.random() > 0.5 ? '1' : '0') + '\n';
        }
        column.textContent = text;
        binaryContainer.appendChild(column);
    }
}

// Create Digital Noise Texture
function createDigitalNoise() {
    const canvas = document.getElementById('noise-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    function drawNoise() {
        const imageData = ctx.createImageData(canvas.width, canvas.height);
        const data = imageData.data;

        for (let i = 0; i < data.length; i += 4) {
            const value = Math.random() * 255;
            data[i] = value;     // Red
            data[i + 1] = value; // Green
            data[i + 2] = value; // Blue
            data[i + 3] = 255;   // Alpha
        }

        ctx.putImageData(imageData, 0, 0);
    }

    // Update noise every 100ms for subtle animation
    setInterval(drawNoise, 100);
    drawNoise();
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    createMatrixRain();
    createBinaryRain();
    createDigitalNoise();
    initializeChat();
});

// Rest of the existing script.js code...
const API_URL = 'http://localhost:5000';
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
let currentMode = 'chat'; // Default mode

function selectMode(mode) {
    currentMode = mode;

    // Update UI Badges
    document.querySelectorAll('.module-badge').forEach(badge => {
        if (badge.dataset.mode === mode) {
            badge.classList.add('active');
        } else {
            badge.classList.remove('active');
        }
    });

    // Update Input Placeholder based on Mode
    const placeholders = {
        'rag': 'Search documents or ask technical queries...',
        'gmail': 'Draft emails, summarize inbox, or generate replies...',
        'linkedin': 'Generate posts, hooks, or optimize profile...',
        'chat': 'Ask me anything... (General Chat)'
    };

    if (messageInput) {
        messageInput.placeholder = placeholders[mode] || placeholders['chat'];
        messageInput.focus();
    }
}
// Initialize
function initializeChat() {
    checkBackendStatus();
    setInterval(checkBackendStatus, 10000); // Auto-check connection every 10s
    setupEventListeners();
    setWelcomeTime();
    selectMode('chat');
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
            body: JSON.stringify({
                query: message,
                mode: currentMode
            }),
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

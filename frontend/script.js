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
    // Remove active class from all tools (legacy, new buttons, and list rows)
    document.querySelectorAll('.tool-item, .tool-icon-btn, .tool-row, .tool-icon-btn-row').forEach(item => {
        item.classList.remove('active');
    });

    // Add active class to selected tool
    if (event && event.currentTarget) {
        const cl = event.currentTarget.classList;
        if (cl.contains('tool-item') || cl.contains('tool-icon-btn') || cl.contains('tool-row') || cl.contains('tool-icon-btn-row')) {
            cl.add('active');
        }
    }

    currentTool = toolName;
    selectMode(toolName); // Integrate with existing selectMode function

    // Show notification
    showToolNotification(toolName);

    // Auto-close toolbox after selection (All devices)
    const toolbox = document.getElementById('aiToolbox');
    if (toolbox && toolbox.classList.contains('open')) {
        toggleToolbox();
    }
}

// Show Tool Selection Notification
function showToolNotification(toolName) {
    const toolNames = {
        document: 'Document Analyzer',
        email: 'Email Summarizer',
        resume: 'Resume Scanner',
        project: 'Project Analyzer',
        linkedin: 'LinkedIn Generator',
        brain: 'Personal Brain',
        chat: 'General Chat'
    };

    // Remove existing notifications
    const existing = document.querySelectorAll('.tool-notification');
    existing.forEach(el => el.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'tool-notification';
    notification.innerHTML = `<span class="mode-icon">⚡</span> Mode Active: <strong>${toolNames[toolName] || toolName}</strong>`;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(13, 13, 13, 0.9);
        border: 1px solid var(--matrix-green);
        color: var(--text-green);
        padding: 10px 25px;
        border-radius: 50px;
        font-family: var(--font-secondary);
        font-size: 0.9rem;
        z-index: 200;
        animation: slideDown 0.5s ease;
        box-shadow: 0 4px 20px rgba(0, 255, 65, 0.2);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        gap: 8px;
    `;

    document.body.appendChild(notification);

    // Persist notification until mode changes (no auto-remove) 
    // or we could auto-remove. User requested "Context-Aware mode indicators".
    // Let's keep it visible but subtle, or maybe move it to the chat header?
    // For now, let's auto-remove after 5s to avoid clutter, but update the UI elsewhere.

    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.5s ease forwards';
        setTimeout(() => notification.remove(), 500);
    }, 4000);
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
const API_URL = 'http://127.0.0.1:8000';
// State Variables
let isProcessing = false;
let isLoading = false;
let loadingInterval;
let isDevMode = false; // Default: User Mode
let isMotionEnabled = true; // Default: Motion On

// PHASE 23: State Stability & Locking
let backendChecksEnabled = true;
let isChatActive = false;
let isDemoMode = false;

// DOM Elements
// DOM Elements
// DOM Elements
const chatInput = document.getElementById('chatInput');
const messagesContainer = document.getElementById('messages');
const aiToolbox = document.getElementById('aiToolbox');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');
const statusText = document.getElementById('status-text');
const charCount = document.getElementById('char-count');
const welcomeTime = document.getElementById('welcome-time');
const uploadZone = document.getElementById('upload-zone');     // New Upload Zone
const fileInput = document.getElementById('file-upload');      // New Input
const modePill = document.createElement('div');

// Initialize Mode Pill
modePill.className = 'mode-pill';
modePill.style.cssText = 'position:absolute; top:-30px; left:50%; transform:translateX(-50%); background:rgba(0,0,0,0.6); padding:4px 12px; border-radius:12px; font-size:0.8rem; color: #00f7ff; border: 1px solid rgba(0,247,255,0.3); z-index:10; opacity:0; transition:opacity 0.3s; pointer-events:none;';
modePill.innerText = 'Mode: General Chat';
if (document.querySelector('.chat-container')) {
    document.querySelector('.chat-container').appendChild(modePill);
}

// Initialize
let currentMode = 'chat'; // Default mode

function showEmptyState() {
    if (messagesContainer.children.length === 0) {
        messagesContainer.innerHTML = `
            <div class="empty-state" id="empty-state">
                <h1 class="welcome-title">👋 Hi Bhuvi</h1>
                <p class="welcome-subtitle">Ask me anything or select a tool to begin.</p>
            </div>
        `;
    }
}

function selectMode(mode) {
    currentMode = mode;
    console.log(`Switched to mode: ${mode}`);

    // Update Upload Zone Visibility
    if (uploadZone) {
        if (mode === 'rag') {
            uploadZone.classList.remove('hidden');
        } else {
            uploadZone.classList.add('hidden');
        }
    }

    // Update Mode Label (Internal)
    const modeName = mode.charAt(0).toUpperCase() + mode.slice(1);
    const modeText = document.getElementById('mode-text');
    if (modeText) {
        modeText.innerText = `${modeName} Assistant`;
        // Optional: Add subtle flash effect
        modeText.parentElement.style.borderColor = 'var(--matrix-green)';
        setTimeout(() => modeText.parentElement.style.borderColor = 'rgba(255,255,255,0.1)', 500);
    }
}

// Function to use prompt chips
function usePrompt(text) {
    if (messageInput) {
        messageInput.value = text;
        messageInput.focus();
        // Optional: Auto-send
        // handleSend();
    }
}


// Setup Upload Listeners
function setupUploadListeners() {
    if (!uploadZone || !fileInput) return;

    // Click to Browse
    uploadZone.addEventListener('click', () => fileInput.click());

    // File Selected
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Drag Over
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('active');
    });

    // Drag Leave
    uploadZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('active');
    });

    // Drop
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('active');
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

// Handle File Upload
async function handleFileUpload(file) {
    // Validate
    const validTypes = ['application/pdf', 'text/plain', 'text/markdown'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.md')) {
        showToolNotification('Invalid file type. Please upload PDF or TXT.');
        return;
    }

    // Show uploading status
    const uploadingMsgId = addMessage(`<div class="loading-dots"><span>.</span><span>.</span><span>.</span></div> Uploading <strong>${file.name}</strong>...`, 'ai');
    showToolNotification(`Uploading ${file.name}...`);

    try {
        const formData = new FormData();
        formData.append('files', file);

        const response = await fetch(`${API_URL}/ingest`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Remove loading message (simulated by replacing content) or just append success
        // Simpler: Just append success message

        if (response.ok) {
            addMessage(`✅ <strong>${file.name}</strong> ingested! <br>Processed ${data.details.chunks_created} chunks. Ready to support answers.`, 'ai');
            showToolNotification('Ingestion Complete');
        } else {
            throw new Error(data.detail || 'Upload failed');
        }

    } catch (error) {
        console.error('Upload Error:', error);
        addMessage(`❌ Failed to upload <strong>${file.name}</strong>.<br><em>${error.message}</em>`, 'ai');
        showToolNotification('Upload Failed');
    }
}
// UX: Focus input
if (messageInput) messageInput.focus();

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

// Initialize
function initializeChat() {
    checkBackendStatus();
    setInterval(checkBackendStatus, 10000); // Auto-check connection every 10s
    setupEventListeners();
    setupUtilityListeners(); // Initialize utility buttons
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
// Check backend status
// Check backend status with Retry Logic (Phase 68)
async function checkBackendStatus(retryCount = 0) {
    // PHASE 23: Stop checks if locked
    if (!backendChecksEnabled) return;

    // Only log on first attempt to avoid spam
    if (retryCount === 0) console.log("Checking backend status...");

    try {
        const controller = new AbortController();
        const id = setTimeout(() => controller.abort(), 5000); // Increased to 5s for grace

        const response = await fetch(`${API_URL}/health`, { signal: controller.signal });
        clearTimeout(id);

        if (response.ok) {
            updateStatus('Online', true);
            hideOfflineOverlay();
        } else {
            console.warn(`Backend returned non-OK status (Attempt ${retryCount + 1})`);
            if (retryCount < 2) {
                // Retry twice before failing
                setTimeout(() => checkBackendStatus(retryCount + 1), 1000);
            } else {
                showOfflineState();
            }
        }
    } catch (error) {
        console.error(`Backend check failed (Attempt ${retryCount + 1}):`, error);
        if (retryCount < 2) {
            // Retry twice before failing
            setTimeout(() => checkBackendStatus(retryCount + 1), 1000);
        } else {
            showOfflineState();
        }
    }
}

// Update status indicator
function updateStatus(text, isOnline) {
    const headerStatus = document.getElementById('system-status-indicator');
    if (headerStatus) {
        if (isOnline) {
            headerStatus.textContent = '● Online';
            headerStatus.className = 'status-indicator-header online';
            document.body.classList.remove('offline-mode', 'demo-mode');
            enableInput(true);
        } else {
            headerStatus.textContent = '● Offline';
            headerStatus.className = 'status-indicator-header offline';
        }
    }
}

// PHASE 21: Offline State Handling
function showOfflineState() {
    // Only show if we aren't already in intentional Demo Mode
    if (document.body.classList.contains('demo-mode')) return;

    document.body.classList.add('offline-mode');
    const overlay = document.getElementById('offline-overlay');
    if (overlay) overlay.style.display = 'flex';

    updateStatus('Offline', false);
    enableInput(false, "Assistant is offline (Demo Mode)");
}

window.retryBackend = async function () {
    const btn = document.querySelector('.primary-btn');
    if (btn) btn.textContent = "Connecting...";

    await checkBackendStatus();

    // If still offline, reset text
    if (document.body.classList.contains('offline-mode')) {
        if (btn) btn.textContent = "Retry Connection";
    }
};

window.enableDemo = function () {
    // PHASE 23: Lock State
    document.body.classList.remove('offline-mode');
    document.body.classList.add('demo-mode');

    isDemoMode = true;
    backendChecksEnabled = false; // Stop checking backend

    const overlay = document.getElementById('offline-overlay');
    if (overlay) overlay.style.display = 'none';

    // Allow interaction
    enableInput(true, "Demo Mode (Mock Responses)");

    // Update Header
    const headerStatus = document.getElementById('system-status-indicator');
    if (headerStatus) {
        headerStatus.textContent = '● Demo Mode'; // Phase 23 Label
        headerStatus.className = 'status-indicator-header offline'; // Keep yellow color
    }
};

function hideOfflineOverlay() {
    document.body.classList.remove('offline-mode');
    const overlay = document.getElementById('offline-overlay');
    if (overlay) overlay.style.display = 'none';
}

function enableInput(enabled, placeholderText) {
    const input = document.getElementById('message-input');
    if (input) {
        input.disabled = !enabled;
        if (placeholderText) input.placeholder = placeholderText;
        if (!enabled) input.value = '';
    }
}

// Setup event listeners
function setupEventListeners() {
    if (sendButton) {
        sendButton.addEventListener('click', handleSend);
    }

    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            // Enter sends, Shift+Enter adds new line
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (!isProcessing) {
                    handleSend();
                } else {
                    console.log("Ignored Enter: processing in progress");
                }
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
                handleSend(); // Auto-send
            }
        });
    });

    if (messageInput) {
        messageInput.addEventListener('input', () => {
            messageInput.style.height = 'auto';
            messageInput.style.height = messageInput.scrollHeight + 'px';
        });
    }
}

// Setup Utility Button Listeners (Settings, Notifications, Voice, Profile)
function setupUtilityListeners() {
    // 1. Voice Mode Button (Speech Recognition)
    const voiceBtn = document.querySelector('.voice-mode-btn');
    if (voiceBtn) {
        // Check browser support
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = "en-US";
            recognition.interimResults = false;
            recognition.continuous = false;

            recognition.onstart = () => {
                voiceBtn.classList.add('active');
                voiceBtn.style.color = '#00f7ff';
                voiceBtn.style.borderColor = '#00f7ff';
                voiceBtn.style.boxShadow = '0 0 15px rgba(0, 247, 255, 0.3)';
                showToolNotification('Listening... 🎙️');
                createAudioVisualizer();
            };

            recognition.onend = () => {
                voiceBtn.classList.remove('active');
                voiceBtn.style.color = '';
                voiceBtn.style.borderColor = '';
                voiceBtn.style.boxShadow = '';
                const visualizer = document.getElementById('audio-visualizer');
                if (visualizer) visualizer.remove();

                // Auto-send if we have text?
                // User might want to edit. Let's focus input.
                if (messageInput && messageInput.value.trim()) {
                    messageInput.focus();
                }
            };

            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                if (messageInput) {
                    // Append if reusing or replace? Replace is standard for short command.
                    messageInput.value = transcript;
                    updateCharCount();
                    // Optional: Auto-Send for "AI Assistant like that" feel?
                    // Let's delay send slightly or just populate. 
                    // User said "mic not ai assistant like that", maybe they expect auto-send?
                    // Let's auto-send for voice commands to feel "assistant-like".
                    setTimeout(() => handleSend(), 500);
                }
            };

            recognition.onerror = (e) => {
                console.error("Voice error:", e.error);
                showToolNotification(`Voice Error: ${e.error}`);
                voiceBtn.classList.remove('active');
            };

            voiceBtn.addEventListener('click', () => {
                if (voiceBtn.classList.contains('active')) {
                    recognition.stop();
                } else {
                    try {
                        recognition.start();
                    } catch (e) {
                        console.log("Recognition error:", e);
                    }
                }
            });
        } else {
            console.warn("Speech Recognition not supported");
            voiceBtn.addEventListener('click', () => {
                showToolNotification('Voice not supported in this browser');
            });
        }
    }

    // 2. Profile Dropdown Logic
    // Handled via inline onclick="toggleProfileMenu()" and global click listener
    window.addEventListener('click', (e) => {
        const dropdown = document.getElementById('profile-dropdown');
        const chip = document.querySelector('.user-profile-chip');
        if (dropdown && chip && !chip.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('active');
        }
    });

    // Make global functions available if not already
    window.toggleProfileMenu = function () {
        const dropdown = document.getElementById('profile-dropdown');
        if (dropdown) {
            dropdown.classList.toggle('active');
        }
    };
}

// --- ADVANCED UI HELPERS ---

// Create Audio Visualizer Overlay
function createAudioVisualizer() {
    const existing = document.getElementById('audio-visualizer');
    if (existing) existing.remove();

    const overlay = document.createElement('div');
    overlay.className = 'audio-visualizer-overlay';
    overlay.id = 'audio-visualizer';

    // Create 5 animated bars
    for (let i = 0; i < 5; i++) {
        const bar = document.createElement('div');
        bar.className = 'visualizer-bar';
        overlay.appendChild(bar);
    }

    // Auto-close after 5 seconds to simulate test
    document.body.appendChild(overlay);
    setTimeout(() => {
        if (document.getElementById('audio-visualizer')) {
            // Optional: Don't auto close if user wants it persistent, 
            // but for demo we keep it clean.
            // overlay.remove(); 
        }
    }, 5000);
}

// Create System Log Terminal
function createSystemLog() {
    if (!isDevMode) {
        showToolNotification('System Logs are hidden (User Mode)');
        return;
    }

    const existing = document.getElementById('system-log');
    if (existing) {
        existing.remove();
        return; // Toggle off
    }
    // ... rest of log creation code (unchanged logic, just guarded) ...
    // For brevity, re-implementing basic log creation here or keeping existing if compatible
    const overlay = document.createElement('div');
    overlay.className = 'system-log-overlay';
    overlay.id = 'system-log';

    overlay.innerHTML = `
        <div class="system-log-header">
            <span>SYSTEM LOG (DEV)</span>
            <span style="cursor:pointer" onclick="this.parentElement.parentElement.remove()">[X]</span>
        </div>
        <div class="system-log-content" id="log-content"></div>
    `;

    document.body.appendChild(overlay);
    // ... simple log simulation ...
    const logContent = overlay.querySelector('#log-content');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.innerHTML = `<span class="log-time">[${new Date().toLocaleTimeString()}]</span> Dev Mode Active. Monitoring events...`;
    logContent.appendChild(entry);
}

// Create Holographic Settings Modal (REAL CONTROLS)
function createSettingsModal() {
    const existing = document.getElementById('holo-settings');
    if (existing) {
        existing.remove();
        return;
    }

    const modal = document.createElement('div');
    modal.className = 'holo-settings-modal';
    modal.id = 'holo-settings';

    modal.innerHTML = `
        <div class="holo-settings-header">
            SYSTEM SETTINGS
        </div>
        
        <div class="setting-row">
            <span class="setting-label">Dev Mode (Show Logs)</span>
            <div class="toggle-switch ${isDevMode ? 'active' : ''}" id="toggle-dev"></div>
        </div>

        <div class="setting-row">
            <span class="setting-label">Reduced Motion</span>
            <div class="toggle-switch ${!isMotionEnabled ? 'active' : ''}" id="toggle-motion"></div>
        </div>

        <button class="action-btn danger" id="btn-clear-chat">Clear Chat History</button>
        <button class="action-btn" onclick="this.parentElement.parentElement.remove()">Close</button>
    `;

    document.body.appendChild(modal);

    // Event Listeners for Settings
    modal.querySelector('#toggle-dev').addEventListener('click', function () {
        isDevMode = !isDevMode;
        this.classList.toggle('active');
        showToolNotification(`Dev Mode: ${isDevMode ? 'ON' : 'OFF'}`);
    });

    modal.querySelector('#toggle-motion').addEventListener('click', function () {
        isMotionEnabled = !isMotionEnabled;
        this.classList.toggle('active');
        const robot = document.querySelector('.robot-img');
        if (robot) {
            robot.style.animation = isMotionEnabled ? 'breathe 8s ease-in-out infinite' : 'none';
        }
        showToolNotification(`Motion: ${isMotionEnabled ? 'ON' : 'OFF'}`);
    });

    modal.querySelector('#btn-clear-chat').addEventListener('click', () => {
        if (confirm('Clear all messages?')) {
            messagesContainer.innerHTML = '';
            showEmptyState();
            modal.remove();
        }
    });
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

    // PHASE 23: Lock UI State on Chat Start
    if (!isChatActive) {
        isChatActive = true;
        backendChecksEnabled = false; // Stop checking
        hideOfflineOverlay(); // Ensure overlay is gone

        // If we were in Demo Mode but user started chatting, keep simulated responses 
        // OR try to use backend if online?
        // JSON Rule: "disableBackendChecks: true", "lockUI: true"
        // If we are effectively "Offline", this will just use Demo Mode logic anyway.
    }

    // PHASE 22: Demo Mode Logic
    if (document.body.classList.contains('demo-mode')) {
        messageInput.value = '';
        messageInput.style.height = 'auto';
        updateCharCount();
        addMessage(message, 'user');

        isProcessing = true;
        showTypingIndicator();

        setTimeout(() => {
            hideTypingIndicator();
            addMessage("👋 Demo Mode Active. Backend is offline. This is a simulated response.", 'assistant');
            isProcessing = false;
        }, 1000);
        return;
    }

    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    updateCharCount();

    // Add user message
    addMessage(message, 'user');

    // Clear empty state if present
    const emptyState = document.querySelector('.empty-state');
    if (emptyState) emptyState.remove();

    // UX: Start Loading State
    isProcessing = true;
    isLoading = true;
    if (sendButton) sendButton.disabled = true;

    // Instant response - No artificial delay
    // showTypingIndicator(); // Optional: Show immediately if needed, or rely on swift fetch

    // Show refined typing indicator
    showTypingIndicator();

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

        // UX: Stop Loading State
        hideTypingIndicator();

        // Add assistant message
        addMessage(data.answer, 'assistant');

    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();

        if (isDevMode) {
            // Show raw technical error ONLY in Dev Mode
            const errorMsg = `
                <div class="system-status-message">
                    <span class="status-icon">⚠️</span>
                    <div class="status-content">
                        <strong>System Error (Dev)</strong>
                        <p>${error.message}</p>
                    </div>
                </div>
            `;
            addMessage(errorMsg, 'assistant', true);
        } else {
            // Friendly Error for User
            const friendlyError = `
                <div class="friendly-error" style="text-align: center; padding: 20px;">
                    <div class="loading-dots" style="font-size: 2rem; margin-bottom: 10px;"></div>
                    <strong style="font-size: 1.1rem; color: var(--matrix-green);">Assistant is reconnecting...</strong>
                    <p style="margin-top: 5px; font-size: 0.9rem; opacity: 0.7;">Please check your connection.</p>
                </div>
            `;
            addMessage(friendlyError, 'assistant', false, true); // isError=false to avoid red box, isHTML=true
        }
    } finally {
        isProcessing = false;
        isLoading = false;
        if (sendButton) sendButton.disabled = false;
        if (messageInput) messageInput.focus();
    }
}

// Show Premium Typing Indicator
function showTypingIndicator() {
    if (!messagesContainer) return;

    // Remove existing if any
    hideTypingIndicator();

    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant-message loading-message';
    loadingDiv.id = 'ai-loading-indicator';

    const avatar = document.createElement('div');
    avatar.className = 'message-avatar pulse-animation';
    avatar.innerHTML = `<img src="logo_green_robot.png" alt="AI" class="bot-avatar-img">`;

    const content = document.createElement('div');
    content.className = 'message-content typing-content';

    // Dots Animation
    const dotsHtml = `
        <div class="typing-dots-container">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    `;

    // Status Text
    const statusHtml = `<div class="status-text" id="status-text-loading">Thinking...</div>`;

    content.innerHTML = dotsHtml + statusHtml;
    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(content);

    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    // Rotate Status Text
    const statuses = ["Thinking...", "Analyzing context...", "Generating response...", "Almost there..."];
    let index = 0;
    const statusElement = document.getElementById('status-text-loading');

    if (statusElement) {
        loadingInterval = setInterval(() => {
            index = (index + 1) % statuses.length;
            statusElement.textContent = statuses[index];
            statusElement.style.opacity = 0;
            setTimeout(() => {
                statusElement.style.opacity = 1;
            }, 200);
        }, 1500);
    }
}

// Hide Typing Indicator
function hideTypingIndicator() {
    const loadingDiv = document.getElementById('ai-loading-indicator');
    if (loadingDiv) {
        loadingDiv.remove();
    }
    if (loadingInterval) {
        clearInterval(loadingInterval);
        loadingInterval = null;
    }
}

// Add message to chat
function addMessage(text, sender, isError = false, isHTML = false) {
    if (!messagesContainer) return;

    // Remove empty state if present
    const emptyState = document.getElementById('empty-state');
    if (emptyState) emptyState.remove();

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    // Avatar Logic
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    if (sender === 'user') {
        // Use premium SVG icon for user
        avatar.innerHTML = `
            <div class="user-avatar-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
        `;
    } else {
        avatar.innerHTML = `<img src="logo_green_robot.png" alt="AI" class="bot-avatar-img">`; // Use actual logo
    }

    const content = document.createElement('div');
    content.className = 'message-content';

    // Only add header for AI messages (to show 'Bhuvi AI' and time)
    // User messages should be compact (text only)
    if (sender === 'ai') {
        const header = document.createElement('div');
        header.className = 'message-header';

        const author = document.createElement('span');
        author.className = 'message-author';
        author.textContent = 'Bhuvi AI';

        const time = document.createElement('span');
        time.className = 'message-time';
        const now = new Date();
        time.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });

        header.appendChild(author);
        header.appendChild(time);
        content.appendChild(header);
    }

    // For User messages, we skip the header to keep it tight.
    // Optionally we can add a tiny timestamp at the bottom later if requested.

    const messageText = document.createElement('div');
    messageText.className = 'message-text';

    if (isError) {
        messageText.innerHTML = `<div class="error-message">⚠️ ${text}</div>`;
    } else if (isHTML) {
        messageText.innerHTML = text;
    } else {
        messageText.innerHTML = formatMessage(text);
    }

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
// ========================================
// PHASE 9: SETUP WIZARD LOGIC
// ========================================

async function checkHealtAndSetup() {
    try {
        const response = await fetch(`${API_URL}/health`);
        // If 500 or specific error, might mean missing keys if we coded it that way.
        // But simplified: checking if we have keys locally or just showing wizard if first time?
        // Let's use a localStorage flag for the wizard to not be annoying, 
        // BUT also verify with backend if possible.
        // For MVP: If localStorage 'setup_complete' is missing, show it.

        if (!localStorage.getItem('setup_complete')) {
            document.getElementById('setupWizard').style.display = 'flex';
        }
    } catch (e) {
        console.warn("Backend check failed, might need setup or is offline");
        document.getElementById('setupWizard').style.display = 'flex';
    }
}

async function saveApiKeys() {
    const geminiKey = document.getElementById('apiKeyInput').value.trim();
    const openaiKey = document.getElementById('openaiKeyInput').value.trim();

    if (!geminiKey) {
        alert("Gemini API Key is required!");
        return;
    }

    const btn = document.querySelector('.primary-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = 'Connecting...';
    btn.disabled = true;

    try {
        const response = await fetch(`${API_URL}/api/setup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                gemini_api_key: geminiKey,
                openai_api_key: openaiKey
            })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('setup_complete', 'true');
            document.getElementById('setupWizard').style.display = 'none';
            showToolNotification('System Connected 🟢');
            setTimeout(() => location.reload(), 1500); // Reload to ensure backend picks up new env
        } else {
            alert("Setup Failed: " + data.detail);
        }
    } catch (error) {
        console.error("Setup error:", error);
        alert("Connection Error. Is backend running?");
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

function startDemoMode() {
    localStorage.setItem('demo_mode', 'true');
    localStorage.setItem('setup_complete', 'true'); // Don't show again
    document.getElementById('setupWizard').style.display = 'none';
    showToolNotification('Entered Demo Mode 🟡');
    isDevMode = true; // Enable logs for demo fun
    // Add visual indicator
    const modeLabel = document.getElementById('mode-text');
    if (modeLabel) modeLabel.innerText += " (DEMO)";
}


// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    // Initial backend check
    checkBackendStatus();
    checkHealtAndSetup(); // Check for wizard

    setInterval(checkBackendStatus, 10000); // Auto-check connection every 10s
    setupEventListeners();
    setupUtilityListeners(); // Initialize utility buttons
    setupUploadListeners();
    setWelcomeTime();

    // Initialize Mode Label
    selectMode('chat');

    // Pause Background Animation on Input Focus
    const input = document.getElementById('message-input');
    if (input) {
        input.addEventListener('focus', () => document.body.classList.add('paused-bg'));
        input.addEventListener('blur', () => document.body.classList.remove('paused-bg'));
    }

    // Set auto-refresh for time
    setInterval(setWelcomeTime, 10000);
});

// ========================================
// GLOBAL EXPORTS (Fix for inline onclick events)
// ========================================
window.selectTool = selectTool;
window.usePrompt = usePrompt;
window.handleSend = handleSend; // For retry button
window.createSettingsModal = createSettingsModal;
window.createSystemLog = createSystemLog;
window.toggleDevMode = () => {
    isDevMode = !isDevMode;
    showToolNotification(`Dev Mode: ${isDevMode ? 'ON' : 'OFF'}`);
};
window.saveApiKeys = saveApiKeys;
window.startDemoMode = startDemoMode;

window.toggleToolbox = toggleToolbox;
window.applySettings = applySettings;



// ========================================
// PHASE 56: GLOBAL FILE HANDLER (ROBUST)
// ========================================

// Exposed function called directly by HTML onchange
window.handleFileUpload = function (input) {
    if (input.files && input.files.length > 0) {
        const file = input.files[0];
        console.log("File Selected:", file.name);

        const attachBtn = document.querySelector('.attach-btn');
        const inputContainer = document.querySelector('.input-container');
        const inputWrapper = document.querySelector('.input-wrapper');

        // Visual Feedback on Button
        if (attachBtn) {
            attachBtn.style.color = '#00ff41';
            attachBtn.style.background = 'rgba(0, 255, 65, 0.1)';
            attachBtn.style.boxShadow = '0 0 15px rgba(0, 255, 65, 0.3)';
        }

        // Create/Update Preview Card
        let preview = document.getElementById('file-preview-pill');
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'file-preview-pill';
            // Styling for "Floating Card" above input
            preview.style.cssText = `
                background: rgba(16, 20, 30, 0.95);
                border: 1px solid rgba(0, 255, 65, 0.3);
                border-left: 3px solid #00ff41;
                color: #fff;
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 0.85rem;
                margin-bottom: 10px;
                margin-left: 4px;
                display: inline-flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
                animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                z-index: 100 !important;
                position: relative;
                min-width: 150px;
                justify-content: space-between;
            `;

            // Insert safely
            if (inputContainer && inputWrapper) {
                inputContainer.insertBefore(preview, inputWrapper);
            } else {
                // Fallback: append to chat shell if container missing
                const shell = document.querySelector('.chat-shell') || document.body;
                shell.appendChild(preview);
            }
        }

        // Set Content
        preview.innerHTML = `
            <div style="display:flex; flex-direction:column;">
                <span style="font-size:0.65rem; color:#00ff41; font-weight:700; letter-spacing:0.5px; text-transform:uppercase;">Attached File</span>
                <span style="display:flex; align-items:center; gap:6px; font-weight:500; margin-top:2px;">
                    <span style="font-size:1.1rem;">📄</span> ${file.name.substring(0, 25)}${file.name.length > 25 ? '...' : ''}
                </span>
            </div>
            <button onclick="window.clearFile(event)" style="background:rgba(255,255,255,0.1); border:none; color:#fff; cursor:pointer; width:24px; height:24px; border-radius:50%; display:flex; align-items:center; justify-content:center; transition:background 0.2s;">
                ×
            </button>
        `;
    }
};

window.clearFile = function (event) {
    if (event) event.stopPropagation();

    const fileInput = document.getElementById('file-upload');
    const preview = document.getElementById('file-preview-pill');
    const attachBtn = document.querySelector('.attach-btn');

    if (fileInput) fileInput.value = '';
    if (preview) preview.remove();
    if (attachBtn) {
        attachBtn.style.color = '';
        attachBtn.style.background = '';
        attachBtn.style.boxShadow = '';
    }
};
// ========================================
// PHASE 57: PERSISTENT HISTORY LOADER
// ========================================
async function loadServerHistory() {
    if (document.body.classList.contains('demo-mode')) return; // Skip in demo mode

    try {
        console.log("Fetching chat history...");
        const response = await fetch('http://localhost:8000/api/history');
        if (!response.ok) throw new Error("History fetch failed");

        const history = await response.json();

        if (history && history.length > 0) {
            console.log(`Loaded ${history.length} messages from history.`);

            // Hide empty state
            const emptyState = document.querySelector('.empty-state');
            if (emptyState) emptyState.style.display = 'none';

            // Render Messages
            history.forEach(msg => {
                // Ensure content is valid string
                if (msg.content) {
                    // Use existing addMessage function
                    // addMessage(text, sender, isError, isHTML)
                    // We assume it handles markdown conversion if implemented, or just plain text
                    // If addMessage expects HTML for markdown, we might need a parser here.
                    // But looking at existing code, addMessage seems to take raw text.
                    addMessage(msg.content, msg.role);
                }
            });

            // Scroll to bottom
            const container = document.querySelector('.messages');
            if (container) {
                setTimeout(() => {
                    container.scrollTop = container.scrollHeight;
                }, 100);
            }
        }
    } catch (e) {
        console.warn("Could not load history (Backend might be offline):", e);
    }
}

// Call on load
document.addEventListener('DOMContentLoaded', loadServerHistory);
// ========================================
// PHASE 58: TOAST FILE PREVIEW (GUARANTEED VISIBILITY)
// ========================================

// Redefine handler to force "Toast" visibility
window.handleFileUpload = function (input) {
    if (input.files && input.files.length > 0) {
        const file = input.files[0];
        console.log("File Selected (Toast Mode):", file.name);

        const attachBtn = document.querySelector('.attach-btn');

        // Visual Feedback on Button
        if (attachBtn) {
            attachBtn.style.color = '#00ff41';
            attachBtn.style.background = 'rgba(0, 255, 65, 0.1)';
            attachBtn.style.boxShadow = '0 0 15px rgba(0, 255, 65, 0.3)';
        }

        // Create/Update Preview Card (Fixed Position Toast)
        let preview = document.getElementById('file-preview-pill');
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'file-preview-pill';
            preview.style.cssText = `
                position: fixed;
                bottom: 120px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(16, 20, 30, 0.95);
                border: 1px solid rgba(0, 255, 65, 0.5);
                border-left: 4px solid #00ff41;
                color: #fff;
                padding: 10px 16px;
                border-radius: 12px;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                animation: slideUpToast 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 99999 !important;
                min-width: 220px;
                backdrop-filter: blur(10px);
            `;

            // Append directly to BODY
            document.body.appendChild(preview);

            // Add animation if missing
            if (!document.getElementById('toast-anim')) {
                const style = document.createElement('style');
                style.id = 'toast-anim';
                style.innerHTML = `
                    @keyframes slideUpToast {
                        from { transform: translate(-50%, 40px); opacity: 0; }
                        to { transform: translate(-50%, 0); opacity: 1; }
                    }
                `;
                document.head.appendChild(style);
            }
        }

        // Set Content
        preview.innerHTML = `
            <div style="display:flex; flex-direction:column;">
                <span style="font-size:0.7rem; color:#00ff41; font-weight:700; letter-spacing:1px; text-transform:uppercase;">Attached Document</span>
                <span style="display:flex; align-items:center; gap:8px; font-weight:600; margin-top:2px; font-size:1rem;">
                    📄 ${file.name.substring(0, 20)}${file.name.length > 20 ? '...' : ''}
                </span>
            </div>
            <button onclick="window.clearFile(event)" style="background:rgba(255,255,255,0.1); border:none; color:#fff; cursor:pointer; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; transition:background 0.2s; font-size:1.2rem;">
                ×
            </button>
        `;
    }
};

// ========================================
// PHASE 65: RICH FILE PREVIEW (ICONS + COLORS)
// ========================================
window.handleFileUpload = function (input) {
    if (input.files && input.files.length > 0) {
        const file = input.files[0];
        console.log("File Selected (Rich Mode):", file.name);

        const attachBtn = document.querySelector('.attach-btn');
        const ext = file.name.split('.').pop().toLowerCase();

        // Define Styling based on extension
        let theme = {
            color: '#00ff41', // Default Green
            icon: '📄',
            label: 'DOCUMENT',
            bg: 'rgba(0, 255, 65, 0.1)'
        };

        if (['pdf'].includes(ext)) {
            theme = { color: '#ff4b4b', icon: '📛', label: 'PDF DOCUMENT', bg: 'rgba(255, 75, 75, 0.15)' };
        } else if (['doc', 'docx'].includes(ext)) {
            theme = { color: '#4b9eff', icon: '📝', label: 'WORD DOCUMENT', bg: 'rgba(75, 158, 255, 0.15)' };
        } else if (['xls', 'xlsx', 'csv'].includes(ext)) {
            theme = { color: '#00ce7c', icon: '📊', label: 'EXCEL SHEET', bg: 'rgba(0, 206, 124, 0.15)' };
        } else if (['ppt', 'pptx'].includes(ext)) {
            theme = { color: '#ffaa00', icon: '📉', label: 'POWERPOINT', bg: 'rgba(255, 170, 0, 0.15)' };
        } else if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(ext)) {
            theme = { color: '#bd00ff', icon: '🖼️', label: 'IMAGE', bg: 'rgba(189, 0, 255, 0.15)' };
        }

        // Visual Feedback on Button
        if (attachBtn) {
            attachBtn.style.color = theme.color;
            attachBtn.style.background = theme.bg;
            attachBtn.style.boxShadow = `0 0 15px ${theme.color}40`;
        }

        // Create/Update Preview Card (Fixed Position Toast)
        let preview = document.getElementById('file-preview-pill');
        if (!preview) {
            preview = document.createElement('div');
            preview.id = 'file-preview-pill';
            preview.style.cssText = `
                position: fixed;
                bottom: 120px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(16, 20, 30, 0.95);
                border: 1px solid ${theme.color}80;
                border-left: 4px solid ${theme.color};
                color: #fff;
                padding: 10px 16px;
                border-radius: 12px;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                animation: slideUpToast 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 99999 !important;
                min-width: 250px;
                backdrop-filter: blur(10px);
            `;

            document.body.appendChild(preview);

            if (!document.getElementById('toast-anim')) {
                const style = document.createElement('style');
                style.id = 'toast-anim';
                style.innerHTML = `
                    @keyframes slideUpToast {
                        from { transform: translate(-50%, 40px); opacity: 0; }
                        to { transform: translate(-50%, 0); opacity: 1; }
                    }
                `;
                document.head.appendChild(style);
            }
        } else {
            // Dynamic Update for existing card
            preview.style.borderColor = `${theme.color}80`;
            preview.style.borderLeftColor = theme.color;
        }

        // Set Content
        preview.innerHTML = `
            <div style="display:flex; flex-direction:column;">
                <span style="font-size:0.7rem; color:${theme.color}; font-weight:700; letter-spacing:1px; text-transform:uppercase;">${theme.label}</span>
                <span style="display:flex; align-items:center; gap:8px; font-weight:600; margin-top:3px; font-size:0.95rem;">
                    <span style="font-size:1.2rem; filter: drop-shadow(0 0 8px ${theme.color}60);">${theme.icon}</span> 
                    ${file.name.substring(0, 22)}${file.name.length > 22 ? '...' : ''}
                </span>
            </div>
            <button onclick="window.clearFile(event)" style="background:rgba(255,255,255,0.1); border:none; color:#fff; cursor:pointer; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; transition:background 0.2s; font-size:1.2rem; margin-left:auto;">
                ×
            </button>
        `;
    }
};
// ========================================
// SETTINGS MODAL FUNCTIONALITY
// ========================================

// Default settings


// Load settings from localStorage or use defaults





// Close settings modal


// Populate settings from saved values


// Apply settings to the application
function applySettings(settings) {
    // Apply dev mode
    if (settings.devMode) {
        isDevMode = true;
        console.log('Developer mode enabled');
    } else {
        isDevMode = false;
    }

    // Apply other settings as needed
    // This can be extended based on your application's needs
}

// Clear chat history




// Delete all data
function deleteAllData() {
    if (confirm('⚠️ WARNING: This will delete ALL your data including chat history, settings, and preferences. This cannot be undone. Are you absolutely sure?')) {
        if (confirm('Final confirmation: Delete everything?')) {
            localStorage.clear();
            showToolNotification('All data deleted. Reloading...');
            setTimeout(() => location.reload(), 1500);
        }
    }
}

// Update slider values in real-time
document.addEventListener('DOMContentLoaded', () => {
    // Temperature slider
    const tempSlider = document.getElementById('temperature');
    const tempValue = document.getElementById('temperatureValue');
    if (tempSlider && tempValue) {
        tempSlider.addEventListener('input', (e) => {
            tempValue.textContent = (e.target.value / 100).toFixed(1);
        });
    }

    // Speech rate slider
    const speechSlider = document.getElementById('speechRate');
    const speechValue = document.getElementById('speechRateValue');
    if (speechSlider && speechValue) {
        speechSlider.addEventListener('input', (e) => {
            speechValue.textContent = (e.target.value / 100).toFixed(1) + 'x';
        });
    }

    // Load settings on page load
    const settings = loadSettings();
    applySettings(settings);
});

// Export functions to window for HTML onclick handlers
window.deleteAllData = deleteAllData;

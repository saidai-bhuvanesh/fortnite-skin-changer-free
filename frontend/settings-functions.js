/**
 * Settings Modal Functions
 * Handles opening, closing, and interaction within the settings modal.
 */

// Make functions globally available
window.openProfileSettings = function () {
    console.log('Opening Profile Settings...');
    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.classList.add('active');
        console.log('Settings Modal Active');
        // Populate settings from storage
        populateSettings();
        // Close profile dropdown if open
        const dropdown = document.getElementById('profile-dropdown');
        if (dropdown) dropdown.classList.remove('active');
    } else {
        console.error('Settings modal element not found!');
        alert('Error: Settings Modal not found. Please refresh the page.');
    }
};

window.closeSettings = function () {
    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.classList.remove('active');
    }
};

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('settingsModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeSettings();
            }
        });
    }
});

// Toggle individual settings
window.toggleSetting = function (element) {
    element.classList.toggle('active');
    // Here you would typically save the setting state
    console.log('Toggled setting:', element.nextElementSibling.innerText, element.classList.contains('active'));
};

// Save settings with animation
window.saveSettings = function () {
    const saveBtn = document.querySelector('.btn-save');
    const originalText = saveBtn.innerText;

    saveBtn.innerText = 'Saved! ✅';
    saveBtn.style.background = '#00ff7f';
    saveBtn.style.color = '#000';

    setTimeout(() => {
        closeSettings();
        // Reset button state after closing
        setTimeout(() => {
            saveBtn.innerText = originalText;
            saveBtn.style.background = '';
            saveBtn.style.color = '';
        }, 500);
    }, 800);
};

// Open API Settings (Setup Wizard)
window.openAPISettings = function () {
    closeSettings();
    const setupWizard = document.getElementById('setupWizard');
    if (setupWizard) {
        setupWizard.style.display = 'flex';
        // Close profile dropdown
        const dropdown = document.getElementById('profile-dropdown');
        if (dropdown) dropdown.classList.remove('active');
    }
};

// Open Theme Settings (Aliases to Profile Settings)
window.openThemeSettings = function () {
    window.openProfileSettings();
};

// Toggle Profile Dropdown
window.toggleProfileDropdown = function () {
    const dropdown = document.getElementById('profile-dropdown');
    if (dropdown) {
        dropdown.classList.toggle('active');
        // Close settings modal if open
        const settings = document.getElementById('settingsModal');
        if (settings) settings.classList.remove('active');
    }
};

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('profile-dropdown');
    const profileSection = document.querySelector('.profile-section');

    if (dropdown && dropdown.classList.contains('active')) {
        if (!dropdown.contains(e.target) && (!profileSection || !profileSection.contains(e.target))) {
            dropdown.classList.remove('active');
        }
    }
});
});

// ========================================
// SETTINGS LOGIC MIGRATED BELOW
// ========================================

// Default settings
const defaultSettings = {
    // AI Model Settings
    aiModel: 'gemini-pro',
    temperature: 0.7,
    maxTokens: 2048,
    streaming: true,

    // Response Customization
    responseTone: 'professional',
    responseFormat: 'detailed',
    codeHighlight: true,
    language: 'en',

    // Voice & Audio
    voiceInput: true,
    tts: false,
    voiceSelection: 'female',
    speechRate: 1.0,
    autoPlay: false,

    // Notifications
    desktopNotif: true,
    sound: true,
    taskAlerts: true,
    errorNotif: true,

    // Data & Privacy
    saveHistory: true,
    autoSave: true,

    // Advanced Features
    devMode: false,
    debugLogs: false,
    customApi: false,
    experimental: false
};

// Load settings from localStorage or use defaults
function loadSettings() {
    const saved = localStorage.getItem('bhuviSettings');
    return saved ? JSON.parse(saved) : { ...defaultSettings };
}

// Save settings to localStorage
function saveSettingsToStorage(settings) {
    localStorage.setItem('bhuviSettings', JSON.stringify(settings));
}

// Populate settings from saved values
function populateSettings() {
    const settings = loadSettings();

    // Helper to safely set value
    const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.value = val;
    };

    // Helper to safely set text
    const setText = (id, txt) => {
        const el = document.getElementById(id);
        if (el) el.textContent = txt;
    };

    // AI Model Settings
    setVal('aiModel', settings.aiModel);
    if (document.getElementById('temperature')) document.getElementById('temperature').value = settings.temperature * 100;
    setText('temperatureValue', settings.temperature.toFixed(1));
    setVal('maxTokens', settings.maxTokens);
    setToggleState('streamingToggle', settings.streaming);

    // Response Customization
    setVal('responseTone', settings.responseTone);
    setVal('responseFormat', settings.responseFormat);
    setToggleState('codeHighlightToggle', settings.codeHighlight);
    setVal('language', settings.language);

    // Voice & Audio
    setToggleState('voiceInputToggle', settings.voiceInput);
    setToggleState('ttsToggle', settings.tts);
    setVal('voiceSelection', settings.voiceSelection);
    if (document.getElementById('speechRate')) document.getElementById('speechRate').value = settings.speechRate * 100;
    setText('speechRateValue', settings.speechRate.toFixed(1) + 'x');
    setToggleState('autoPlayToggle', settings.autoPlay);

    // Notifications
    setToggleState('desktopNotifToggle', settings.desktopNotif);
    setToggleState('soundToggle', settings.sound);
    setToggleState('taskAlertsToggle', settings.taskAlerts);
    setToggleState('errorNotifToggle', settings.errorNotif);

    // Data & Privacy
    setToggleState('saveHistoryToggle', settings.saveHistory);
    setToggleState('autoSaveToggle', settings.autoSave);

    // Advanced Features
    setToggleState('devModeToggle', settings.devMode);
    setToggleState('debugLogsToggle', settings.debugLogs);
    setToggleState('customApiToggle', settings.customApi);
    setToggleState('experimentalToggle', settings.experimental);
}

// Set toggle switch state
function setToggleState(toggleId, isActive) {
    const toggle = document.getElementById(toggleId);
    if (toggle) {
        if (isActive) {
            toggle.classList.add('active');
        } else {
            toggle.classList.remove('active');
        }
    }
}

// Toggle individual setting (Override simple version)
window.toggleSetting = function (element) {
    element.classList.toggle('active');
};

// Save settings (Override simple version)
window.saveSettings = function () {
    const getValue = (id) => {
        const el = document.getElementById(id);
        return el ? el.value : '';
    };

    const isChecked = (id) => {
        const el = document.getElementById(id);
        return el ? el.classList.contains('active') : false;
    };

    const settings = {
        // AI Model Settings
        aiModel: getValue('aiModel'),
        temperature: parseFloat(getValue('temperature') || 70) / 100,
        maxTokens: parseInt(getValue('maxTokens') || 2048),
        streaming: isChecked('streamingToggle'),

        // Response Customization
        responseTone: getValue('responseTone'),
        responseFormat: getValue('responseFormat'),
        codeHighlight: isChecked('codeHighlightToggle'),
        language: getValue('language'),

        // Voice & Audio
        voiceInput: isChecked('voiceInputToggle'),
        tts: isChecked('ttsToggle'),
        voiceSelection: getValue('voiceSelection'),
        speechRate: parseFloat(getValue('speechRate') || 100) / 100,
        autoPlay: isChecked('autoPlayToggle'),

        // Notifications
        desktopNotif: isChecked('desktopNotifToggle'),
        sound: isChecked('soundToggle'),
        taskAlerts: isChecked('taskAlertsToggle'),
        errorNotif: isChecked('errorNotifToggle'),

        // Data & Privacy
        saveHistory: isChecked('saveHistoryToggle'),
        autoSave: isChecked('autoSaveToggle'),

        // Advanced Features
        devMode: isChecked('devModeToggle'),
        debugLogs: isChecked('debugLogsToggle'),
        customApi: isChecked('customApiToggle'),
        experimental: isChecked('experimentalToggle')
    };

    saveSettingsToStorage(settings);

    // Apply settings if app function exists
    if (window.applySettings) {
        window.applySettings(settings);
    }

    // UI Feedback
    const saveBtn = document.querySelector('.btn-save');
    if (saveBtn) {
        const originalText = saveBtn.innerText;
        saveBtn.innerText = 'Saved! ✅';
        saveBtn.style.background = '#00ff7f';
        saveBtn.style.color = '#000';
        setTimeout(() => {
            closeSettings();
            setTimeout(() => {
                saveBtn.innerText = originalText;
                saveBtn.style.background = '';
                saveBtn.style.color = '';
            }, 500);
        }, 800);
    } else {
        closeSettings();
    }
};

// Reset settings to defaults
window.resetSettings = function () {
    if (confirm('Are you sure you want to reset all settings to defaults?')) {
        saveSettingsToStorage(defaultSettings);
        populateSettings();
        alert('Settings reset to defaults');
    }
};

// Clear chat history
window.clearChatHistory = function () {
    if (confirm('Are you sure you want to clear all chat history? This cannot be undone.')) {
        const messagesContainer = document.getElementById('messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = `
                <div class="empty-state" id="empty-state">
                    <h1 class="welcome-title">👋 Hi Bhuvi</h1>
                    <p class="welcome-subtitle">Ask me anything or select a tool to begin.</p>
                </div>
            `;
        }
        localStorage.removeItem('chatHistory');
        alert('Chat history cleared');
    }
};

// Export chat data
window.exportChatData = function () {
    const messages = [];
    const messageElements = document.querySelectorAll('.message');

    messageElements.forEach(msg => {
        const sender = msg.classList.contains('user-message') ? 'user' : 'assistant';
        const text = msg.querySelector('.message-text')?.textContent || '';
        messages.push({ sender, text });
    });

    const dataStr = JSON.stringify(messages, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `bhuvi-chat-export-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
};

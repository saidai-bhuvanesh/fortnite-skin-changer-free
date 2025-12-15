# Bhuvi AI Assistant - Quick Start Guide

## 🚀 Starting the Backend (Recommended Method)

### Option 1: Simple Start (Recommended)
Double-click `start_backend.bat` in the project folder.

### Option 2: With Auto-Restart Monitor
```bash
python monitor_backend.py
```
This will automatically restart the backend if it crashes.

### Option 3: Manual Start
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## ✅ Verify Backend is Running

1. Open browser to: http://localhost:8000
2. You should see: `{"message": "Bhuvi AI Assistant API is running"}`

---

## 🌐 Open the Chatbot UI

Open in browser: `file:///C:/Users/bhuva/Downloads/NP/frontend/index.html`

Or double-click `frontend/index.html`

---

## 🔧 Troubleshooting

### Backend Shows "Offline"
1. Refresh browser (F5)
2. Check if backend is running: http://localhost:8000
3. Restart backend using `start_backend.bat`

### Ollama Not Working
1. Make sure Ollama is installed and running
2. Check: http://localhost:11434
3. Pull model: `ollama pull gemma2:2b`

### Port 8000 Already in Use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /F /PID <PID_NUMBER>
```

---

## 📝 Configuration

Edit `.env` file to change settings:
- `LLM_PROVIDER=ollama` (use Ollama)
- `OLLAMA_MODEL=gemma2:2b` (fast 2-3s responses)
- `OLLAMA_BASE_URL=http://localhost:11434`

---

## 🎨 New Features (Final Release)

✨ **Rich File Preview**: Upload PDFs, Excel, Word, or Images and get instant color-coded identification (Red/Green/Blue cards).
✨ **Holographic Voice Mode**: Click the microphone to see a 3D Audio Visualizer while you speak.
✨ **Smart Shortcuts**: Type "hlo", "hi", "help" for instant responses.
✨ **Robust Connection**: Backend now auto-retries connection failures without crashing the UI.

---

## 💡 Tips

- **Shortcuts**: Type "hlo" to wake up the bot instantly.
- **Voice**: Click the Mic icon 🎙️ to use speech-to-text.
- **Files**: Drag & Drop or click the Paperclip 📎 to analyze documents.
- **Backend Monitor**: Run `monitor_backend.py` to ensure 24/7 uptime.

---

## 🆘 Troubleshooting

### Backend Shows "Reconnecting..."
1. Don't panic! The system will auto-retry 3 times.
2. If it persists, check if the backend terminal is open.
3. Restart using `start_backend.bat`.

### Voice Not Working?
- Ensure you are using Chrome/Edge.
- Check microphone permissions.

### Check Logs
- Backend: `backend/logs/app.log`
- LLM: `backend/logs/llm_chat.log`

Backend should show:
```
✅ All modules initialized successfully!
INFO: Uvicorn running on http://0.0.0.0:8000
```

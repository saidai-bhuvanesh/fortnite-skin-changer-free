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

## 🎨 Features

✨ Ultra-premium 3D holographic UI
⚡ Fast responses (2-3 seconds with gemma2:2b)
🌌 Floating hexagons and particle effects
💎 Glassmorphism design
🎯 RAG, Gmail, LinkedIn integration

---

## 💡 Tips

- Keep backend running in background
- Use `monitor_backend.py` for auto-restart
- Refresh browser if status shows offline
- Backend auto-reloads on code changes

---

## 🆘 Need Help?

Check logs:
- Backend: `backend/logs/app.log`
- LLM: `backend/logs/llm_chat.log`

Backend should show:
```
✅ Initialized Ollama (unlimited local AI): gemma2:2b
INFO: Uvicorn running on http://0.0.0.0:8000
```

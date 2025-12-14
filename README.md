# 🤖 Bhuvi AI Assistant - Personal AI Command Center

> **Status**: Verified Stable | **Theme**: Cyber Nebula (v2.5)

A next-generation Personal AI Assistant featuring a holographic glassmorphism UI, multi-agent backend, and seamless integration with Gmail, LinkedIn, and local documents (RAG).

## ✨ Key Features

-   **🧠 Multi-Agent Core**: Powered by Gemini 1.5 Flash (with OpenAI fallback).
-   **🎨 Holographic UI**: Ultra-premium glassmorphism design with "Cyber Nebula" aesthetics.
-   **📂 RAG Engine**: Drag & Drop PDF/TXT ingestion for document analysis.
-   **🎙️ Voice Command**: Native speech recognition with visual audio feedback.
-   **🔌 Smart Integrations**:
    -   **Gmail**: Summarize emails, draft replies.
    -   **LinkedIn**: Generate viral posts and hooks.
-   **🧙‍♂️ Setup Wizard**: Automatic API key configuration for first-time users.

## 🚀 Quick Start

### 1. Backend Setup (FastAPI)
Ensure you have Python 3.9+ installed.

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the server (Auto-reloads)
uvicorn main:app --reload
```
*Server will start at `http://127.0.0.1:8000`*

### 2. Frontend Setup
Simply open `frontend/index.html` in your browser.
*(Recommended: Use "Live Server" extension in VS Code for best experience)*

### 3. First Run & Configuration
1.  Launch the web interface.
2.  If no API keys are found, the **Setup Wizard** will appear.
3.  Enter your **Gemini API Key** (Required).
4.  (Optional) Enter OpenAI Key for advanced fallback.
5.  Click **Connect Core**.

## 🛠️ Tech Stack
-   **Frontend**: Vanilla JS, Modern CSS3 (Variables, Animations), Glassmorphism.
-   **Backend**: FastAPI, LangChain, ChromaDB (Vector Store).
-   **AI**: Google Gemini 1.5 Flash, OpenAI GPT-4o.

## 📝 Developer Notes
-   **Dev Mode**: Click the user profile -> "Dev Mode" to see raw system logs.
-   **Motion Reduced**: Toggle in Settings for accessibility.
-   **Health Check**: GET `http://127.0.0.1:8000/health`

---
*Created by Bhuvaneshwar for Portfolio Showcase 2025*

# 🤖 Bhuvi Personal AI Assistant

A powerful multi-agent AI Personal Assistant that combines RAG (Retrieval-Augmented Generation), Gmail automation, LinkedIn content generation, and intelligent query routing.

![Status](https://img.shields.io/badge/status-ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

## ✨ Features

- **📚 RAG Engine** - Search and retrieve information from your personal documents (PDFs, DOCX, TXT)
- **📧 Gmail Integration** - Fetch, summarize, and manage your emails automatically
- **💼 LinkedIn Bot** - Generate professional posts, captions, and comments with AI
- **💬 Intelligent Chat** - General AI assistant powered by Google Gemini
- **🔀 Smart Routing** - Automatically routes queries to the right module
- **🎨 Premium UI** - Beautiful dark-mode web interface with glassmorphism

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│          Web Chat UI (Frontend)             │
└──────────────────┬──────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────┐
│        FastAPI Backend (Router)             │
│  ┌─────────────────────────────────────┐   │
│  │  Intent Detection & Query Routing   │   │
│  └─────────────────────────────────────┘   │
└─────┬──────┬──────┬──────┬─────────────────┘
      │      │      │      │
   ┌──▼─┐ ┌─▼──┐ ┌─▼──┐ ┌─▼───┐
   │RAG │ │Gmail│ │Lin│ │LLM  │
   │    │ │     │ │kedIn│ │Chat│
   └────┘ └────┘ └────┘ └────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- (Optional) Gmail OAuth credentials for email features
- (Optional) LinkedIn API credentials for auto-posting

### Installation

1. **Clone or navigate to the project directory**

```bash
cd c:\Users\bhuva\Downloads\NP
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Copy `.env.example` to `.env` and fill in your API keys:

```bash
# Minimum required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (for Gmail features)
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret

# Optional (for LinkedIn auto-posting)
LINKEDIN_CLIENT_ID=your_linkedin_client_id
```

4. **Add your documents (Optional)**

Place your PDFs, DOCX, or TXT files in the `docs/` folder for RAG to search.

5. **Start the backend server**

```bash
cd backend
python main.py
```

Or using uvicorn directly:

```bash
uvicorn backend.main:app --reload --port 8000
```

6. **Open the web UI**

Open `frontend/index.html` in your browser, or use a local server:

```bash
# Using Python
cd frontend
python -m http.server 8080

# Then visit: http://localhost:8080
```

## 📖 Usage Examples

### RAG Queries (Document Search)
```
"Summarize my resume"
"What projects have I worked on?"
"Tell me about my Python experience"
```

### Gmail Queries
```
"Check my unread emails"
"Summarize my inbox"
"Show me recent emails"
```

### LinkedIn Queries
```
"Create a LinkedIn post about AI automation"
"Generate a corporate post about machine learning"
"Rewrite this caption: [your text]"
```

### General Chat
```
"Explain recursion"
"What is RAG?"
"Help me understand vector databases"
```

## 🔧 API Endpoints

### Main Chat Endpoint
```http
POST /chat
Content-Type: application/json

{
  "query": "Your question here",
  "context": "Optional context"
}
```

### Ingest Documents
```http
POST /ingest
Content-Type: application/json

{
  "docs_path": "./docs"  // Optional, defaults to configured path
}
```

### Health Check
```http
GET /
```

### System Stats
```http
GET /stats
```

## 📁 Project Structure

```
NP/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   └── modules/
│       ├── llm_chat.py         # LLM integration
│       ├── rag_engine.py       # RAG system
│       ├── gmail_reader.py     # Gmail automation
│       ├── linkedin_bot.py     # LinkedIn content gen
│       ├── document_processor.py
│       └── answer_builder.py
├── frontend/
│   ├── index.html              # Web UI
│   ├── styles.css              # Premium styling
│   └── script.js               # Chat functionality
├── docs/                        # Your documents for RAG
├── requirements.txt
├── .env.example
└── README.md
```

## 🎯 Module Breakdown

### 1. RAG Engine
- Extracts text from PDF, DOCX, TXT
- Creates vector embeddings using sentence-transformers
- Stores in ChromaDB for semantic search
- Retrieves relevant context for queries

### 2. Gmail Reader
- OAuth 2.0 authentication
- Fetches emails with filters
- Parses subject, sender, body
- LLM-powered summarization

### 3. LinkedIn Bot
- AI-generated posts by topic/style
- Caption improvement
- Hashtag generation
- Comment creation

### 4. LLM Chat
- Google Gemini integration
- Intent extraction for routing
- General conversation handling
- Context-aware responses

### 5. Answer Builder
- Merges multi-module responses
- Citations and source tracking
- Cohesive answer formatting

## 🔐 Gmail OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials as `credentials.json`
6. Place in project root directory
7. First run will open browser for authorization

## 🎨 UI Features

- **Dark Mode** - Easy on the eyes with gradient backgrounds
- **Glassmorphism** - Modern translucent design
- **Real-time Status** - See which modules are active
- **Typing Indicators** - Know when AI is thinking
- **Quick Actions** - One-click common queries
- **Responsive** - Works on desktop and mobile

## 🛠️ Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Ensure `.env` file exists with valid API keys

### Frontend can't connect
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify API_BASE_URL in script.js matches backend

### RAG not finding documents
- Run document ingestion: POST to `/ingest`
- Check `docs/` folder has supported files
- View logs in `logs/rag_engine.log`

### Gmail errors
- Ensure `credentials.json` is in root directory
- Delete `token.pickle` and re-authorize
- Check Gmail API is enabled in Google Cloud Console

## 📊 Performance

- **RAG Search**: ~100-200ms for 5 chunks
- **Gmail Fetch**: ~1-2s for 10 emails
- **LinkedIn Generation**: ~2-3s per post
- **LLM Response**: ~1-3s depending on prompt

## 🔮 Future Enhancements

- [ ] Conversation history persistence
- [ ] Voice input/output
- [ ] Mobile app (Flutter)
- [ ] Multi-language support
- [ ] Calendar integration
- [ ] WhatsApp automation
- [ ] Advanced analytics dashboard

## 📝 License

MIT License - feel free to use this for your personal projects!

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📧 Contact

Made with ❤️ by Bhuvanesh

---

**Note**: This AI assistant is designed for personal use. Keep your API keys secure and never commit them to version control!

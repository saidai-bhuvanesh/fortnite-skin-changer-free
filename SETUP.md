# Quick Setup Guide - Bhuvi AI Assistant

Follow these simple steps to get your AI Assistant running!

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including FastAPI, ChromaDB, Gemini, etc.

## Step 2: Configure API Key

1. Get your Google Gemini API key from: https://makersuite.google.com/app/apikey

2. Copy the `.env.example` file to create your `.env`:
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Step 3: (Optional) Add Your Documents

Place any PDFs, Word docs, or text files in the `docs/` folder for the RAG engine to search.

## Step 4: Start the Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ All modules initialized successfully!
```

## Step 5: Open the Frontend

Option A - Direct file open:
- Open `frontend/index.html` in your web browser

Option B - Using Python server (recommended):
```bash
cd frontend
python -m http.server 8080
```
Then visit: http://localhost:8080

## Step 6: Test It Out!

Try these queries:
- "What can you help me with?"
- "Create a LinkedIn post about AI"
- "Explain what RAG is"

## Gmail Setup (Optional)

For email features:

1. Go to https://console.cloud.google.com
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` and place in project root
6. Update `.env` with client ID and secret
7. First run will open browser for authorization

## Troubleshooting

**Backend won't start?**
- Make sure you're in the `backend/` directory
- Check that Python 3.9+ is installed: `python --version`
- Verify `.env` file exists with valid API key

**Frontend can't connect?**
- Ensure backend is running on port 8000
- Check browser console for errors (F12)
- Try using localhost:8080 instead of direct file open

**RAG not working?**
- Add documents to the `docs/` folder
- Call the `/ingest` endpoint to process documents
- Check logs in `logs/rag_engine.log`

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start backend
cd backend && python main.py

# Start frontend (separate terminal)
cd frontend && python -m http.server 8080

# Check backend status
curl http://localhost:8000/

# Ingest documents
curl -X POST http://localhost:8000/ingest
```

## Next Steps

- Add your resume/documents to `docs/` folder
- Set up Gmail OAuth for email features
- Customize the UI in `frontend/styles.css`
- Explore different LLM models in `backend/config.py`

Enjoy your Personal AI Assistant! 🚀

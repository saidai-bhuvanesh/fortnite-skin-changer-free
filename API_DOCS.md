# API Endpoints Documentation

Base URL: `http://localhost:8000`

## Main Endpoints

### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "online",
  "service": "Bhuvi Personal AI Assistant",
  "version": "1.0.0",
  "modules": {
    "llm": "gemini",
    "rag": "enabled",
    "gmail": "enabled",
    "linkedin": "enabled"
  },
  "rag_stats": {
    "total_chunks": 0,
    "collection_name": "personal_docs"
  }
}
```

### 2. Chat Interface
```http
POST /chat
Content-Type: application/json
```

**Request Body:**
```json
{
  "query": "Your question or command here",
  "context": "Optional additional context"
}
```

**Response:**
```json
{
  "answer": "The AI-generated response",
  "sources": ["resume.pdf", "notes.txt"],
  "modules_used": ["rag", "chat"],
  "primary_intent": "rag",
  "metadata": {}
}
```

**Intent Types:**
- `rag` - Document search queries
- `gmail` - Email-related requests
- `linkedin` - LinkedIn content generation
- `general` - General chat

**Example Queries:**
```json
// RAG Query
{"query": "Summarize my resume"}

// Gmail Query
{"query": "Check my unread emails"}

// LinkedIn Query
{"query": "Create a LinkedIn post about AI automation"}

// Multi-module Query
{"query": "Check my emails and create a LinkedIn post about the most important one"}
```

### 3. Document Ingestion
```http
POST /ingest
Content-Type: application/json
```

**Request Body:**
```json
{
  "docs_path": "./docs"  // Optional, defaults to configured path
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Ingested 5 documents (78 chunks)",
  "details": {
    "documents_processed": 5,
    "chunks_created": 78,
    "status": "success"
  }
}
```

### 4. System Statistics
```http
GET /stats
```

**Response:**
```json
{
  "rag": {
    "total_chunks": 78,
    "collection_name": "personal_docs",
    "db_path": "./chroma_db"
  },
  "gmail_unread": 5,
  "modules_active": {
    "llm": true,
    "rag": true,
    "gmail": true,
    "linkedin": true
  }
}
```

## Module-Specific Behaviors

### RAG Module
Activated when query contains:
- Questions about personal documents
- "resume", "portfolio", "projects"
- "my", "I", referring to personal information

**Returns:**
- Answer based on document context
- List of source documents
- Relevance-ranked chunks

### Gmail Module
Activated when query contains:
- "email", "inbox", "mail"
- "unread", "messages"
- "check my", "summarize my"

**Requires:**
- Gmail OAuth credentials configured
- `credentials.json` in project root

**Returns:**
- Email summaries
- Sender information
- Email count

### LinkedIn Module
Activated when query contains:
- "linkedin", "post", "caption"
- "professional", "content"
- "hashtags", "generate"

**Supports:**
- Post generation (various styles)
- Caption improvement
- Hashtag generation
- Comment creation

**Styles:**
- corporate
- motivational
- technical
- storytelling
- thought_leadership

### General Chat
Activated for:
- Questions not matching other intents
- Explanations and knowledge
- General conversation

## Error Responses

```json
{
  "answer": "Error message here",
  "error": "Detailed error description",
  "modules_used": [],
  "primary_intent": "error"
}
```

**Common Error Codes:**
- `400` - Bad Request (empty query, invalid format)
- `500` - Internal Server Error (module failure, API error)

## Rate Limiting

No rate limiting currently implemented. Use responsibly to avoid API quota issues.

## Authentication

No authentication required for local use. Add authentication middleware for production deployment.

## CORS

Configured origins (can be modified in `.env`):
- http://localhost:3000
- http://localhost:8080
- http://127.0.0.1:5500

## Testing with cURL

```bash
# Health check
curl http://localhost:8000/

# Send chat message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What can you help me with?"}'

# Ingest documents
curl -X POST http://localhost:8000/ingest

# Get stats
curl http://localhost:8000/stats
```

## Testing with JavaScript

```javascript
// Send chat message
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'Create a LinkedIn post about AI'
  })
});

const data = await response.json();
console.log(data.answer);
```

"""
FastAPI Main Application - AI Personal Assistant Backend
Routes queries to appropriate modules and returns combined answers
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from loguru import logger
import sys

from config import settings
from modules.llm_chat import LLMChat
from modules.rag_engine import RAGEngine
from modules.gmail_reader import GmailReader
from modules.linkedin_bot import LinkedInBot
from modules.answer_builder import AnswerBuilder

# Configure logger
logger.remove()
logger.add(sys.stdout, level=settings.log_level)
logger.add(f"logs/{settings.log_file}", rotation="10 MB")

# Initialize FastAPI app
app = FastAPI(
    title="Bhuvi Personal AI Assistant",
    description="Multi-agent AI assistant with RAG, Gmail, LinkedIn automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global module instances
llm_chat = None
rag_engine = None
gmail_reader = None
linkedin_bot = None
answer_builder = None

# Request/Response models
class ChatRequest(BaseModel):
    query: str
    context: Optional[str] = None
    mode: Optional[str] = "chat"

class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
    modules_used: List[str]
    primary_intent: str
    metadata: Optional[Dict] = None

class IngestRequest(BaseModel):
    docs_path: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialize all modules on startup"""
    global llm_chat, rag_engine, gmail_reader, linkedin_bot, answer_builder

    logger.info("Starting AI Personal Assistant...")

    # Validate API keys
    api_keys = settings.validate_api_keys()
    logger.info(f"API Keys configured: {api_keys}")

    try:
        # -------------------------------
        # Initialize LLM (FIXED VERSION)
        # -------------------------------
        # Force Ollama mode (unlimited local AI)
        active_llm = "ollama"
        logger.info(f"Using LLM provider: {active_llm}")

        if active_llm == "gemini":
            llm_chat = LLMChat(
                provider="gemini",
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=settings.use_ollama_fallback
            )
            logger.info(f"Initialized Gemini with model: {settings.gemini_model}")
            if settings.use_ollama_fallback:
                logger.info(f"✅ Ollama fallback enabled: {settings.ollama_model}")
        elif active_llm == "ollama":
            llm_chat = LLMChat(
                provider="ollama",
                api_key="",  # Ollama doesn't need API key
                model="",
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=False  # Already using Ollama
            )
            logger.info(f"✅ Initialized Ollama (unlimited local AI): {settings.ollama_model}")
        else:
            llm_chat = LLMChat(
                provider="openai",
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )

        # Initialize RAG Engine
        logger.info("Initializing RAG Engine...")
        rag_engine = RAGEngine(
            chroma_db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model
        )

        # Initialize Gmail Reader (if configured)
        if api_keys["gmail"]:
            logger.info("Initializing Gmail Reader...")
            gmail_reader = GmailReader()
        else:
            logger.warning("Gmail credentials not configured - Gmail features disabled")

        # Initialize LinkedIn Bot
        logger.info("Initializing LinkedIn Bot...")
        linkedin_bot = LinkedInBot(llm_chat)

        # Initialize Answer Builder
        answer_builder = AnswerBuilder(llm_chat)

        logger.info("✅ All modules initialized successfully!")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise


@app.get("/")
async def root():
    """Health check endpoint"""
    api_keys = settings.validate_api_keys()
    rag_stats = rag_engine.get_stats() if rag_engine else {}

    return {
        "status": "online",
        "service": "Bhuvi Personal AI Assistant",
        "version": "1.0.0",
        "modules": {
            "llm": settings.get_active_llm(),
            "rag": "enabled",
            "gmail": "enabled" if api_keys["gmail"] else "disabled (configure credentials)",
            "linkedin": "enabled"
        },
        "rag_stats": rag_stats
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - routes queries to appropriate modules"""
    try:
        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        logger.info(f"📩 User Query: {query}")

        # Extract intent
        if request.mode and request.mode != "chat":
            # Explicit mode selected by user
            primary_intent = request.mode
            secondary_intents = []
            logger.info(f"Using explicit mode: {primary_intent}")
        else:
            # Auto-detect intent from query (Chat Mode)
            intent_data = llm_chat.extract_intent(query)
            primary_intent = intent_data["primary_intent"]
            secondary_intents = intent_data.get("secondary_intents", [])

        logger.info(f"Final Intent: {primary_intent}, Secondary: {secondary_intents}")

        # Route to modules
        module_responses = {}

        # RAG Module
        if primary_intent == "rag" or "rag" in secondary_intents:
            logger.info("Querying RAG engine...")
            rag_response = rag_engine.answer_query(query, llm_chat, top_k=settings.rag_top_k)
            module_responses["rag"] = rag_response

        # Gmail Module
        if primary_intent == "gmail" or "gmail" in secondary_intents:
            if gmail_reader:
                logger.info("Fetching emails...")
                email_data = gmail_reader.fetch_emails(max_results=settings.gmail_max_results)

                if email_data["emails"]:
                    summary = gmail_reader.summarize_emails(email_data["emails"], llm_chat)
                    module_responses["gmail"] = {
                        "summary": summary,
                        "count": email_data["count"]
                    }
                else:
                    module_responses["gmail"] = {
                        "summary": "No emails found matching your criteria.",
                        "count": 0
                    }
            else:
                module_responses["gmail"] = {
                    "summary": "Gmail integration is not configured. Please set up Gmail credentials.",
                    "count": 0
                }

        # LinkedIn Module
        if primary_intent == "linkedin" or "linkedin" in secondary_intents:
            logger.info("Generating LinkedIn content...")

            if "comment" in query.lower():
                comment = linkedin_bot.generate_comment(query)
                module_responses["linkedin"] = {"comment": comment}
            elif "rewrite" in query.lower() or "improve" in query.lower():
                improved = linkedin_bot.rewrite_caption(query)
                module_responses["linkedin"] = improved
            else:
                post = linkedin_bot.generate_post(
                    topic=query,
                    style="corporate",
                    length="medium"
                )
                module_responses["linkedin"] = post

        # General Chat (fallback)
        if primary_intent == "general" or not module_responses:
            logger.info("Using general chat...")
            chat_response = llm_chat.chat(query, context=request.context)
            module_responses["chat"] = chat_response

        # Build final answer
        final_answer = answer_builder.build_answer(
            query,
            module_responses,
            primary_intent
        )

        logger.info(f"Response built using modules: {final_answer['modules_used']}")
        
        return ChatResponse(**final_answer)
    
    except HTTPException as he:
        # Re-raise HTTP exceptions
        raise he
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        error_str = str(e)
        
        # Check for quota/rate limit errors
        if "429" in error_str or "quota" in error_str.lower() or "rate limit" in error_str.lower():
            raise HTTPException(
                status_code=429,
                detail="API quota exceeded. The chatbot has temporarily reached its usage limit. Please wait 1-2 minutes and try again, or contact the administrator to upgrade the API tier for unlimited access."
            )
        
        # Format other errors nicely
        error_response = answer_builder.format_error(error_str, request.query)
        return ChatResponse(**error_response)


@app.post("/ingest")
async def ingest_documents(request: IngestRequest):
    """Ingest documents into RAG engine"""
    try:
        docs_path = request.docs_path or settings.rag_docs_path

        logger.info(f"Starting document ingestion from: {docs_path}")

        result = rag_engine.ingest_documents(
            docs_path,
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap
        )

        return {
            "status": "success",
            "message": f"Ingested {result['documents_processed']} documents ({result['chunks_created']} chunks)",
            "details": result
        }

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = {
            "rag": rag_engine.get_stats() if rag_engine else {},
            "gmail_unread": gmail_reader.get_unread_count() if gmail_reader else 0,
            "modules_active": {
                "llm": llm_chat is not None,
                "rag": rag_engine is not None,
                "gmail": gmail_reader is not None,
                "linkedin": linkedin_bot is not None
            }
        }
        return stats

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

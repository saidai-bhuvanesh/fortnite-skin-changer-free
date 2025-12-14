"""
FastAPI Main Application - AI Personal Assistant Backend
Routes queries to appropriate modules and returns combined answers
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
from loguru import logger
import sys
import shutil
import os

# PHASE 59: FIX FOR RUNNING FROM 'backend' DIRECTORY
# Ensure the project root is in sys.path so 'backend.config' imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.config import settings
# Imports moved to startup_event to prevent import-time hangs
from backend.modules.llm_chat import LLMChat
from backend.modules.rag_engine import RAGEngine
from backend.modules.gmail_reader import GmailReader
from backend.modules.linkedin_bot import LinkedInBot
from backend.modules.answer_builder import AnswerBuilder

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
class SetupRequest(BaseModel):
    gemini_api_key: str
    openai_api_key: Optional[str] = None

@app.post("/api/setup")
async def setup_api_keys(request: SetupRequest):
    """Save API keys to .env and reload settings"""
    try:
        env_path = Path(__file__).parent.parent / ".env"
        
        # Read existing content
        if env_path.exists():
            content = env_path.read_text().splitlines()
        else:
            content = []

        # Helper to update or add key
        def update_line(key, value):
            updated = False
            for i, line in enumerate(content):
                if line.startswith(f"{key}="):
                    content[i] = f"{key}={value}"
                    updated = True
                    break
            if not updated:
                content.append(f"{key}={value}")

        # Update Keys
        if request.gemini_api_key:
            update_line("GEMINI_API_KEY", request.gemini_api_key)
        if request.openai_api_key:
            update_line("OPENAI_API_KEY", request.openai_api_key)

        # Write back
        env_path.write_text("\n".join(content))
        
        # Reload settings (simplified approach for immediate effect)
        # Note: Ideally we'd re-instantiate settings, but for this simple app, 
        # we might rely on the next request picking it up or restart. 
        # For now, let's try to update os.environ as well for current process.
        os.environ["GEMINI_API_KEY"] = request.gemini_api_key
        if request.openai_api_key:
            os.environ["OPENAI_API_KEY"] = request.openai_api_key
            
        return {"status": "success", "message": "API Keys saved. You may need to restart if issues persist."}
    except Exception as e:
        logger.error(f"Setup failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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

# @app.on_event("startup")
async def _disabled_startup_event():
    """Initialize all modules on startup"""
    global llm_chat, rag_engine, gmail_reader, linkedin_bot, answer_builder
    
    # Lazy imports


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
        elif active_llm == "ollama":
            llm_chat = LLMChat(
                provider="ollama",
                api_key="",  # Ollama doesn't need API key
                model="",
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=False
            )
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

        # Initialize Gmail Reader
        if api_keys["gmail"]:
            gmail_reader = GmailReader()

        # Initialize LinkedIn Bot
        linkedin_bot = LinkedInBot(llm_chat)

        # Initialize Answer Builder
        answer_builder = AnswerBuilder(llm_chat)

        logger.info("✅ All modules initialized successfully!")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        raise

@app.get("/")
async def root():
    return await health_check()

@app.get("/health")
async def health_check():
    api_keys = settings.validate_api_keys()
    rag_stats = rag_engine.get_stats() if rag_engine else {}
    return {
        "status": "online",
        "service": "Bhuvi Personal AI Assistant",
        "modules": {
            "llm": settings.get_active_llm(),
            "rag": "enabled"
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

async def ingest_documents(files: List[UploadFile] = File(...)):
    """Ingest uploaded documents into RAG engine"""
    try:
        saved_count = 0
        docs_path = settings.rag_docs_path
        
        # Ensure docs directory exists
        if not os.path.exists(docs_path):
            os.makedirs(docs_path)

        # Save uploaded files
        for file in files:
            file_location = f"{docs_path}/{file.filename}"
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(file.file, file_object)
            saved_count += 1
            logger.info(f"Saved file: {file.filename}")

        logger.info(f"Starting ingestion for {saved_count} files from: {docs_path}")

        result = rag_engine.ingest_documents(
            docs_path,
            chunk_size=settings.rag_chunk_size,
            chunk_overlap=settings.rag_chunk_overlap
        )

        return {
            "status": "success",
            "message": f"Successfully ingested {result['documents_processed']} documents ({result['chunks_created']} chunks)",
            "details": result
        }

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

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

from backend.modules.history import HistoryManager

# Global module instances
llm_chat = None
rag_engine = None
gmail_reader = None
linkedin_bot = None
answer_builder = None
history_manager = None

@app.on_event("startup")
async def startup_event():
    """Initialize all modules on startup"""
    global llm_chat, rag_engine, gmail_reader, linkedin_bot, answer_builder, history_manager

    logger.info("Starting AI Personal Assistant...")

    # Validate API keys
    api_keys = settings.validate_api_keys()
    logger.info(f"API Keys configured: {api_keys}")

    try:
        # Initialize History Manager
        history_manager = HistoryManager()
        
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
        elif active_llm == "ollama":
            llm_chat = LLMChat(
                provider="ollama",
                api_key="",  # Ollama doesn't need API key
                model="",
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=False
            )
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

        # Initialize Gmail Reader
        if api_keys["gmail"]:
            gmail_reader = GmailReader()
        
        # Initialize LinkedIn Bot (Mock for speed if not needed, but keeping for now)
        linkedin_bot = LinkedInBot(llm_chat)

        # Initialize Answer Builder
        answer_builder = AnswerBuilder(llm_chat)

        logger.info("✅ All modules initialized successfully!")

    except Exception as e:
        logger.error(f"❌ Startup error: {e}")
        # DO NOT RAISE. This keeps the server running so we can see the UI.
        # raise 

@app.get("/api/history")
async def get_history():
    """Get chat history for the frontend"""
    if history_manager:
        return history_manager.load_history()
    return []

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint - routes queries to appropriate modules"""
    try:
        # Emergency Check: If modules failed to load
        if not llm_chat or not history_manager:
            return ChatResponse(
                answer="⚠️ **Critical System Error**: The AI modules are not initialized.\n\n"
                       "Please check the backend terminal for error logs.",
                modules_used=["system"],
                primary_intent="error"
            )

        query = request.query.strip()

        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        # 1. Retrieve Conversation History (Memory)
        history_context = history_manager.get_context_string(limit=3) # Short context for speed
        full_context = f"{history_context}\n{request.context}" if request.context else history_context
        
        logger.info(f"📩 User Query: {query}")

        # 2. Extract intent (Optimized Prompt)
        if request.mode and request.mode != "chat":
            primary_intent = request.mode
            secondary_intents = []
        else:
            # Pass short history to help intent extraction understand follow-ups
            # intent_data = llm_chat.extract_intent(query) 
            # Optimization: Basic keyword check to skip LLM for simple greetings
            if query.lower() in ["hi", "hello", "hey", "help"]:
                 primary_intent = "general"
                 secondary_intents = []
            else:
                 intent_data = llm_chat.extract_intent(query)
                 primary_intent = intent_data["primary_intent"]
                 secondary_intents = intent_data.get("secondary_intents", [])

        logger.info(f"Final Intent: {primary_intent}")

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
                email_data = gmail_reader.fetch_emails(max_results=settings.gmail_max_results)
                if email_data["emails"]:
                    summary = gmail_reader.summarize_emails(email_data["emails"], llm_chat)
                    module_responses["gmail"] = {"summary": summary, "count": email_data["count"]}
                else:
                    module_responses["gmail"] = {"summary": "No emails found.", "count": 0}
            else:
                module_responses["gmail"] = {"summary": "Gmail not configured.", "count": 0}

        # LinkedIn Module
        if primary_intent == "linkedin" or "linkedin" in secondary_intents:
            if "comment" in query.lower():
                comment = linkedin_bot.generate_comment(query)
                module_responses["linkedin"] = {"comment": comment}
            else:
                post = linkedin_bot.generate_post(topic=query, style="corporate", length="medium")
                module_responses["linkedin"] = post

        # General Chat (fallback) - WITH MEMORY
        if primary_intent == "general" or not module_responses:
            logger.info("Using general chat with memory...")
            chat_response = llm_chat.chat(query, context=full_context)
            module_responses["chat"] = chat_response

        # Build final answer
        final_answer = answer_builder.build_answer(query, module_responses, primary_intent)

        # 3. SAVE INTERACTION TO MEMORY
        history_manager.save_interaction(query, final_answer['answer'])

        return ChatResponse(**final_answer)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# PHASE 63: RESTOREED HEALTH CHECK
@app.get("/health")
async def health_check():
    """Explicit health check endpoint"""
    # Simply return OK to signal online status
    return {
        "status": "online",
        "service": "Bhuvi Personal AI Assistant",
        "modules": {
            "llm": "active" if llm_chat else "failed",
            "history": "active" if history_manager else "failed"
        }
    }

@app.get("/")
async def root():
    return await health_check()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )

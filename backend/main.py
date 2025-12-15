"""
FastAPI Main Application - AI Personal Assistant Backend
Refactored for Stability, Cleanliness, and Modular Architecture.
Phase 74: Critical Rewrite
"""

import sys
import os
import shutil
from typing import Optional, Dict, List
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger

# -------------------------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------------------------
# Ensure backend modules can be imported accurately
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from backend.config import settings
from backend.modules.llm_chat import LLMChat
from backend.modules.rag_engine import RAGEngine
from backend.modules.gmail_reader import GmailReader
from backend.modules.linkedin_bot import LinkedInBot
from backend.modules.answer_builder import AnswerBuilder
from backend.modules.history import HistoryManager

# -------------------------------------------------------------------------
# LOGGING CONFIGURATION
# -------------------------------------------------------------------------
logger.remove()
logger.add(sys.stdout, level=settings.log_level)
logger.add(f"logs/{settings.log_file}", rotation="10 MB")

# -------------------------------------------------------------------------
# APP INITIALIZATION
# -------------------------------------------------------------------------
app = FastAPI(
    title="Bhuvi Personal AI Assistant",
    description="Multi-agent AI assistant with RAG, Gmail, LinkedIn automation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------------
# STATE MANAGEMENT
# -------------------------------------------------------------------------
class BackendState:
    """Manages the state of all AI modules to avoid global variable clutter."""
    def __init__(self):
        self.llm_chat: Optional[LLMChat] = None
        self.rag_engine: Optional[RAGEngine] = None
        self.gmail_reader: Optional[GmailReader] = None
        self.linkedin_bot: Optional[LinkedInBot] = None
        self.answer_builder: Optional[AnswerBuilder] = None
        self.history_manager: Optional[HistoryManager] = None
        self.is_initialized = False

    def initialize(self):
        """Initialize all modules."""
        logger.info("🚀 Starting AI Personal Assistant Modules...")
        
        # 1. API Key Validation
        api_keys = settings.validate_api_keys()
        logger.info(f"🔑 API Keys: {api_keys}")

        # 2. History Manager
        self.history_manager = HistoryManager()

        # 3. LLM Setup (Force Ollama/Local preference)
        active_llm = "ollama"  # Defaulting to local for robustness
        logger.info(f"🤖 Using LLM Provider: {active_llm}")
        
        if active_llm == "gemini":
            self.llm_chat = LLMChat(
                provider="gemini",
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=settings.use_ollama_fallback
            )
        elif active_llm == "ollama":
            self.llm_chat = LLMChat(
                provider="ollama",
                api_key="",
                model="",
                ollama_url=settings.ollama_base_url,
                ollama_model=settings.ollama_model,
                use_ollama_fallback=False
            )
        else:
            self.llm_chat = LLMChat(
                provider="openai",
                api_key=settings.openai_api_key,
                model=settings.openai_model
            )

        # 4. RAG Engine
        logger.info("📚 Initializing RAG Engine...")
        self.rag_engine = RAGEngine(
            chroma_db_path=settings.chroma_db_path,
            embedding_model=settings.embedding_model
        )

        # 5. Gmail
        if api_keys["gmail"]:
            self.gmail_reader = GmailReader()
            logger.info("📧 Gmail Module: Active")

        # 6. LinkedIn
        self.linkedin_bot = LinkedInBot(self.llm_chat)
        logger.info("💼 LinkedIn Module: Active")

        # 7. Answer Builder
        self.answer_builder = AnswerBuilder(self.llm_chat)
        
        self.is_initialized = True
        logger.info("✅ All modules initialized successfully!")

state = BackendState()

@app.on_event("startup")
async def startup_event():
    try:
        state.initialize()
    except Exception as e:
        logger.error(f"❌ Startup Critical Error: {e}")
        # We checked earlier: raising here kills the Uvicorn process.
        # We suppress it so the server can start and frontend can show error messages.
        pass 

# -------------------------------------------------------------------------
# DATA MODELS
# -------------------------------------------------------------------------
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

class SetupRequest(BaseModel):
    gemini_api_key: str
    openai_api_key: Optional[str] = None

# -------------------------------------------------------------------------
# ENDPOINTS
# -------------------------------------------------------------------------

@app.get("/")
@app.get("/health")
async def health_check():
    """Service Health Check."""
    return {
        "status": "online",
        "service": "Bhuvi Personal AI Assistant",
        "initialized": state.is_initialized,
        "modules": {
            "llm": "active" if state.llm_chat else "failed",
            "history": "active" if state.history_manager else "failed"
        }
    }

@app.get("/api/history")
async def get_history():
    """Retrieve chat history."""
    if state.history_manager:
        return state.history_manager.load_history()
    return []

@app.post("/api/setup")
async def setup_api_keys(request: SetupRequest):
    """Update API Keys in .env."""
    try:
        env_path = Path(__file__).parent.parent / ".env"
        # Simple append/replace logic
        lines = []
        if env_path.exists():
            lines = env_path.read_text().splitlines()
        
        new_lines = []
        keys_updated = {"GEMINI_API_KEY": False, "OPENAI_API_KEY": False}
        
        for line in lines:
            if line.startswith("GEMINI_API_KEY=") and request.gemini_api_key:
                new_lines.append(f"GEMINI_API_KEY={request.gemini_api_key}")
                keys_updated["GEMINI_API_KEY"] = True
            elif line.startswith("OPENAI_API_KEY=") and request.openai_api_key:
                new_lines.append(f"OPENAI_API_KEY={request.openai_api_key}")
                keys_updated["OPENAI_API_KEY"] = True
            else:
                new_lines.append(line)
        
        if not keys_updated["GEMINI_API_KEY"] and request.gemini_api_key:
            new_lines.append(f"GEMINI_API_KEY={request.gemini_api_key}")
        if not keys_updated["OPENAI_API_KEY"] and request.openai_api_key:
            new_lines.append(f"OPENAI_API_KEY={request.openai_api_key}")
            
        env_path.write_text("\n".join(new_lines))
        
        # Hot update env vars
        if request.gemini_api_key: os.environ["GEMINI_API_KEY"] = request.gemini_api_key
        if request.openai_api_key: os.environ["OPENAI_API_KEY"] = request.openai_api_key
        
        return {"status": "success", "message": "Keys updated!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main Chat Logic with Fallbacks and Optimizations."""
    try:
        # 1. State Verification
        if not state.is_initialized or not state.llm_chat:
            return ChatResponse(
                answer="⚠️ **System Warning**: AI Modules are not active. Please check the backend console.",
                modules_used=["system"],
                primary_intent="error"
            )

        query = request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Empty query")

        logger.info(f"📩 Query: {query}")

        # 2. History Context
        history_context = ""
        if state.history_manager:
            history_context = state.history_manager.get_context_string(limit=3)
        
        full_context = f"{history_context}\n{request.context}" if request.context else history_context

        # 3. Intent Determination
        primary_intent = "general"
        secondary_intents = []
        module_responses = {}

        # OPTIMIZATION: Instant Greetings (Zero-Latency)
        shortcuts = ["hlo", "hi", "hello", "hey", "help", "hola", "greetings", "namaste"]
        if query.lower() in shortcuts:
            primary_intent = "greeting"
        
        # Explicit Mode Override
        elif request.mode and request.mode != "chat":
            primary_intent = request.mode
        
        # LLM Detection (Safe)
        else:
            try:
                intent_data = state.llm_chat.extract_intent(query)
                primary_intent = intent_data["primary_intent"]
                secondary_intents = intent_data.get("secondary_intents", [])
            except Exception as e:
                logger.warning(f"Intent Extraction Failed: {e}")
                primary_intent = "general"

        logger.info(f"🏷️ Intent: {primary_intent}")

        # 4. Module Execution
        
        # --- GREETING ---
        if primary_intent == "greeting":
            module_responses["chat"] = (
                "Hello! 👋 I'm **Bhuvi**, your holographic AI Assistant.\n\n"
                "I can help you with:\n"
                "- 📄 **Document Analysis** (RAG)\n"
                "- 📧 **Email Summaries** (Gmail)\n"
                "- 💼 **LinkedIn Posts**\n"
                "- 💬 **General Chat**\n\n"
                "How can I help you today?"
            )

        # --- RAG ---
        elif (primary_intent == "rag" or "rag" in secondary_intents) and state.rag_engine:
            logger.info("🔍 Running RAG...")
            module_responses["rag"] = state.rag_engine.answer_query(
                query, state.llm_chat, top_k=settings.rag_top_k
            )

        # --- GMAIL ---
        elif (primary_intent == "gmail" or "gmail" in secondary_intents):
            if state.gmail_reader:
                logger.info("📧 Checking Gmail...")
                email_data = state.gmail_reader.fetch_emails(max_results=settings.gmail_max_results)
                if email_data["emails"]:
                    summary = state.gmail_reader.summarize_emails(email_data["emails"], state.llm_chat)
                    module_responses["gmail"] = {"summary": summary, "count": email_data["count"]}
                else:
                    module_responses["gmail"] = {"summary": "No matching emails found.", "count": 0}
            else:
                module_responses["gmail"] = {"summary": "Gmail not configured.", "count": 0}

        # --- LINKEDIN ---
        elif (primary_intent == "linkedin" or "linkedin" in secondary_intents) and state.linkedin_bot:
            logger.info("💼 Generating LinkedIn Content...")
            if "comment" in query.lower():
                res = state.linkedin_bot.generate_comment(query)
                module_responses["linkedin"] = {"comment": res}
            else:
                res = state.linkedin_bot.generate_post(query)
                module_responses["linkedin"] = res

        # --- GENERAL CHAT (Fallback) ---
        if primary_intent == "general" or (not module_responses and primary_intent != "greeting"):
            logger.info("💬 General Chat...")
            try:
                chat_res = state.llm_chat.chat(query, context=full_context)
                module_responses["chat"] = chat_res
            except Exception as e:
                logger.error(f"LLM Chat Error: {e}")
                module_responses["chat"] = {
                    "answer": "⚠️ **I'm having trouble connecting to my brain right now.**\n"
                              "This seems to be a network or quota issue. Please check the logs."
                }

        # 5. Build Answer
        if state.answer_builder:
            final_answer = state.answer_builder.build_answer(query, module_responses, primary_intent)
        else:
            # Emergency fallback if builder missing
            final_answer = {
                "answer": str(module_responses),
                "modules_used": list(module_responses.keys()),
                "primary_intent": primary_intent
            }

        # 6. Save History
        if state.history_manager:
            state.history_manager.save_interaction(query, final_answer['answer'])

        return ChatResponse(**final_answer)

    except Exception as e:
        logger.error(f"🔥 Critical Chat Error: {e}")
        # Return a valid response structure even on crash
        return ChatResponse(
            answer=f"⚠️ **Internal Server Error**: {str(e)}",
            modules_used=["error"],
            primary_intent="error"
        )

@app.post("/api/ingest")
async def ingest_docs(files: List[UploadFile] = File(...)):
    """Ingest uploaded files."""
    try:
        if not state.rag_engine:
            raise HTTPException(status_code=503, detail="RAG Engine not initialized")
            
        saved_count = 0
        docs_path = settings.rag_docs_path
        os.makedirs(docs_path, exist_ok=True)

        for file in files:
            file_loc = f"{docs_path}/{file.filename}"
            with open(file_loc, "wb+") as f:
                shutil.copyfileobj(file.file, f)
            saved_count += 1
        
        result = state.rag_engine.ingest_documents(
            docs_path, 
            chunk_size=settings.rag_chunk_size, 
            chunk_overlap=settings.rag_chunk_overlap
        )
        
        return {"status": "success", "message": f"Processed {saved_count} files.", "details": result}
    except Exception as e:
        logger.error(f"Ingest Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

"""
Configuration management for the AI Personal Assistant
Loads environment variables and provides centralized settings
"""

import os
from pathlib import Path
from typing import Literal, List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # LLM Configuration
    llm_provider: Literal["gemini", "openai", "ollama", "both"] = "gemini"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    openai_api_key: str = ""
    
    # Ollama Configuration (Local AI - Unlimited)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"
    use_ollama_fallback: bool = True
    openai_model: str = "gpt-4-turbo-preview"
    
    # Vector Database
    chroma_db_path: str = "./chroma_db"
    embedding_model: str = "all-MiniLM-L6-v2"
    
    # Gmail API
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_redirect_uri: str = "http://localhost:8000/gmail/callback"
    gmail_max_results: int = 10
    gmail_summary_length: int = 150
    
    # LinkedIn API
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    linkedin_redirect_uri: str = "http://localhost:8000/linkedin/callback"
    
    # Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:5500,http://localhost:5500"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "app.log"
    
    # RAG Configuration
    rag_chunk_size: int = 1000
    rag_chunk_overlap: int = 200
    rag_top_k: int = 3
    rag_docs_path: str = "./docs"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins into list, handling wildcard"""
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    def validate_api_keys(self) -> dict[str, bool]:
        """Check which API keys are configured"""
        return {
            "gemini": bool(self.gemini_api_key and self.gemini_api_key != "your_gemini_api_key_here"),
            "openai": bool(self.openai_api_key and self.openai_api_key != "your_openai_api_key_here"),
            "gmail": bool(self.gmail_client_id and self.gmail_client_id != "your_gmail_client_id.apps.googleusercontent.com"),
            "linkedin": bool(self.linkedin_client_id and self.linkedin_client_id != "your_linkedin_client_id"),
        }
    
    def get_active_llm(self) -> str:
        """Determine which LLM to use based on provider setting and available keys"""
        api_keys = self.validate_api_keys()
        
        # Ollama doesn't need API keys - always available if selected
        if self.llm_provider == "ollama":
            return "ollama"
        elif self.llm_provider == "gemini" and api_keys["gemini"]:
            return "gemini"
        elif self.llm_provider == "openai" and api_keys["openai"]:
            return "openai"
        elif self.llm_provider == "both":
            # Prefer Gemini, fallback to OpenAI
            if api_keys["gemini"]:
                return "gemini"
            elif api_keys["openai"]:
                return "openai"
        
        raise ValueError(
            f"No valid LLM API key found for provider '{self.llm_provider}'. "
            "Please configure GEMINI_API_KEY or OPENAI_API_KEY in .env file."
        )

# Global settings instance
settings = Settings()

# Create necessary directories
Path(settings.chroma_db_path).mkdir(parents=True, exist_ok=True)
Path(settings.rag_docs_path).mkdir(parents=True, exist_ok=True)
Path("logs").mkdir(exist_ok=True)

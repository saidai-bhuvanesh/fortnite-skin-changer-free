"""
LLM Chat Module - General conversation handler
Supports both Google Gemini and OpenAI GPT
"""

import google.generativeai as genai
from openai import OpenAI
import ollama
from typing import Optional, List, Dict
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/llm_chat.log", rotation="10 MB")

class LLMChat:
    """LLM client for general conversations and RAG-enhanced responses"""
    
    def __init__(self, provider: str = "gemini", api_key: str = "", model: str = "",
                 ollama_url: str = "http://localhost:11434", ollama_model: str = "llama3.1",
                 use_ollama_fallback: bool = True):
        """
        Initialize LLM client
        
        Args:
            provider: "gemini", "openai", or "ollama"
            api_key: API key for the provider
            model: Model name to use
            ollama_url: Ollama server URL
            ollama_model: Ollama model name
            use_ollama_fallback: Enable automatic Ollama fallback
        """
        self.provider = provider
        self.model = model
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.use_ollama_fallback = use_ollama_fallback
        
        if provider == "gemini":
            genai.configure(api_key=api_key)
            self.client = genai.GenerativeModel(model)
            logger.info(f"Initialized Gemini model: {model}")
        elif provider == "openai":
            self.client = OpenAI(api_key=api_key)
            logger.info(f"Initialized OpenAI model: {model}")
        elif provider == "ollama":
            self.client = ollama.Client(host=ollama_url)
            logger.info(f"Initialized Ollama model: {ollama_model}")
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
    
    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            prompt: User query or instruction
            system_prompt: System instructions (context)
            temperature: Creativity level (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        try:
            if self.provider == "gemini":
                return self._generate_gemini(prompt, system_prompt, temperature, max_tokens)
            elif self.provider == "ollama":
                return self._generate_ollama(prompt, system_prompt, temperature, max_tokens)
            else:
                return self._generate_openai(prompt, system_prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def _generate_gemini(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using Google Gemini"""
        # Combine system prompt with user prompt
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser Query: {prompt}"
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        try:
            # Try primary Gemini model
            response = self.client.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            # Check for quota/rate limit errors
            if "429" in error_str or "quota" in error_str.lower() or "resource_exhausted" in error_str.lower():
                logger.warning(f"Gemini quota exceeded: {e}")
                
                # Try Ollama fallback if enabled
                if self.use_ollama_fallback:
                    logger.info("🔄 Switching to Ollama (unlimited local AI)")
                    try:
                        return self._generate_ollama(prompt, system_prompt, temperature, max_tokens)
                    except Exception as ollama_error:
                        logger.error(f"Ollama fallback failed: {ollama_error}")
                        raise Exception("Both Gemini and Ollama failed. Please check your setup.")
                else:
                    raise
            else:
                # Re-raise non-quota errors
                raise
    
    def _generate_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using Ollama (local)"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat(
            model=self.ollama_model,
            messages=messages,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        
        return response['message']['content']
    
    def _generate_openai(
        self,
        prompt: str,
        system_prompt: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate response using OpenAI GPT"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """
        Summarize long text into a concise summary
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length in words
            
        Returns:
            Summarized text
        """
        system_prompt = f"Summarize the following text in {max_length} words or less. Be concise and capture key points."
        return self.generate_response(text, system_prompt=system_prompt, temperature=0.3)
    
    def extract_intent(self, query: str) -> Dict[str, any]:
        """
        Extract intent from user query for routing
        
        Args:
            query: User's question/command
            
        Returns:
            Dict with intent classification
        """
        system_prompt = """Analyze the user query and classify it into one or more categories:
        - rag: Questions about personal documents, resume, projects, portfolio
        - gmail: Email-related requests (check, summarize, draft)
        - linkedin: LinkedIn content creation, posts, captions
        - general: General questions, explanations, conversations
        
        Return ONLY a JSON object with:
        {
            "primary_intent": "category",
            "secondary_intents": ["category1", "category2"],
            "confidence": 0.0-1.0
        }
        
        Examples:
        "Summarize my resume" -> {"primary_intent": "rag", "secondary_intents": [], "confidence": 0.95}
        "Check my emails" -> {"primary_intent": "gmail", "secondary_intents": [], "confidence": 0.9}
        "Create a LinkedIn post about AI" -> {"primary_intent": "linkedin", "secondary_intents": [], "confidence": 0.95}
        "Check emails and create a post about it" -> {"primary_intent": "gmail", "secondary_intents": ["linkedin"], "confidence": 0.85}
        """
        
        response = self.generate_response(
            query,
            system_prompt=system_prompt,
            temperature=0.2,
            max_tokens=200
        )
        
        # Parse JSON response
        try:
            import json
            # Extract JSON from response (handle cases where LLM adds extra text)
            if "{" in response and "}" in response:
                json_start = response.index("{")
                json_end = response.rindex("}") + 1
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback: treat as general query
                return {"primary_intent": "general", "secondary_intents": [], "confidence": 0.5}
        except Exception as e:
            logger.warning(f"Intent extraction failed: {e}")
            return {"primary_intent": "general", "secondary_intents": [], "confidence": 0.5}
    
    def chat(self, query: str, context: Optional[str] = None) -> str:
        """
        Simple chat interface
        
        Args:
            query: User's message
            context: Optional context from other modules
            
        Returns:
            Assistant's response
        """
        system_prompt = "You are a helpful AI personal assistant. Be concise, friendly, and informative."
        
        if context:
            system_prompt += f"\n\nContext: {context}"
        
        return self.generate_response(query, system_prompt=system_prompt)

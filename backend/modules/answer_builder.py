"""
Answer Builder - Combine and format responses from multiple modules
"""

from typing import Dict, List, Optional
from loguru import logger
import sys

# Configure logger
logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("logs/answer_builder.log", rotation="10 MB")

class AnswerBuilder:
    """Build final answers by combining outputs from multiple modules"""
    
    def __init__(self, llm_chat):
        """
        Initialize answer builder
        
        Args:
            llm_chat: LLMChat instance for merging responses
        """
        self.llm_chat = llm_chat
    
    def build_answer(
        self,
        query: str,
        module_responses: Dict[str, any],
        primary_intent: str
    ) -> Dict[str, any]:
        """
        Build final answer from module responses
        
        Args:
            query: Original user query
            module_responses: Dict of responses from each module
            primary_intent: Primary intent detected
            
        Returns:
            Final structured answer
        """
        # Single module response
        if len(module_responses) == 1:
            return self._format_single_response(
                query,
                module_responses,
                primary_intent
            )
        
        # Multi-module response - need to merge
        return self._merge_responses(
            query,
            module_responses,
            primary_intent
        )
    
    def _format_single_response(
        self,
        query: str,
        module_responses: Dict[str, any],
        primary_intent: str
    ) -> Dict[str, any]:
        """Format response from a single module"""
        module_name = list(module_responses.keys())[0]
        response = module_responses[module_name]
        
        # RAG response
        if module_name == "rag":
            return {
                "answer": response["answer"],
                "sources": response.get("sources", []),
                "modules_used": ["rag"],
                "primary_intent": primary_intent
            }
        
        # Gmail response
        elif module_name == "gmail":
            return {
                "answer": response["summary"] if "summary" in response else response,
                "email_count": response.get("count", 0),
                "modules_used": ["gmail"],
                "primary_intent": primary_intent
            }
        
        # LinkedIn response
        elif module_name == "linkedin":
            # Format LinkedIn post nicely
            if "full_post" in response:
                answer = f"{response['full_post']}\n\n---\nStyle: {response['style']} | Word count: {response['word_count']}"
            else:
                answer = response.get("improved", response.get("comment", str(response)))
            
            return {
                "answer": answer,
                "modules_used": ["linkedin"],
                "primary_intent": primary_intent,
                "metadata": response
            }
        
        # General chat
        elif module_name == "chat":
            return {
                "answer": response,
                "modules_used": ["chat"],
                "primary_intent": primary_intent
            }
        
        # Unknown module
        return {
            "answer": str(response),
            "modules_used": [module_name],
            "primary_intent": primary_intent
        }
    
    def _merge_responses(
        self,
        query: str,
        module_responses: Dict[str, any],
        primary_intent: str
    ) -> Dict[str, any]:
        """Merge responses from multiple modules using LLM"""
        
        # Build context from all module responses
        context_parts = []
        
        for module, response in module_responses.items():
            if module == "rag":
                context_parts.append(f"**From Your Documents:**\n{response['answer']}")
                if response.get("sources"):
                    context_parts.append(f"Sources: {', '.join(response['sources'])}")
            
            elif module == "gmail":
                summary = response.get("summary", str(response))
                context_parts.append(f"**From Your Emails:**\n{summary}")
            
            elif module == "linkedin":
                if "full_post" in response:
                    context_parts.append(f"**LinkedIn Post Generated:**\n{response['full_post']}")
                else:
                    context_parts.append(f"**LinkedIn Content:**\n{str(response)}")
            
            elif module == "chat":
                context_parts.append(f"**General Information:**\n{response}")
        
        combined_context = "\n\n".join(context_parts)
        
        # Use LLM to create cohesive answer
        system_prompt = f"""You are synthesizing information from multiple sources to answer a user's query.

User Query: {query}

Information from different modules:
{combined_context}

Create a cohesive, well-structured answer that:
1. Addresses the user's query completely
2. Integrates information from all sources smoothly
3. Cites sources where appropriate
4. Is clear and easy to read

Your synthesized answer:"""
        
        merged_answer = self.llm_chat.generate_response(
            "",
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=800
        )
        
        # Extract sources
        sources = []
        if "rag" in module_responses:
            sources.extend(module_responses["rag"].get("sources", []))
        
        return {
            "answer": merged_answer,
            "sources": sources if sources else None,
            "modules_used": list(module_responses.keys()),
            "primary_intent": primary_intent,
            "merged": True
        }
    
    def format_error(self, error_message: str, query: str) -> Dict[str, any]:
        """
        Format error responses in a user-friendly way
        
        Args:
            error_message: Technical error message
            query: User's original query
            
        Returns:
            Formatted error response
        """
        # Detect quota/rate limit errors
        if "429" in error_message or "quota" in error_message.lower() or "rate limit" in error_message.lower():
            friendly_message = """I apologize, but I've temporarily reached my API usage limit. This happens with free tier AI services.

**What you can do:**
• Wait 1-2 minutes and try again (quotas reset automatically)
• Your question: "{query}"

I'm still here and ready to help once the limit resets! 💬""".format(query=query)
        
        # Detect authentication errors
        elif "401" in error_message or "api key" in error_message.lower() or "authentication" in error_message.lower():
            friendly_message = """I'm having trouble connecting to my AI service due to an authentication issue.

**This usually means:**
• The API key needs to be updated
• The service configuration needs attention

Please check with the system administrator."""
        
        # Generic friendly error
        else:
            friendly_message = f"""I apologize, but I encountered an unexpected issue while processing your request.

**Your question:** {query}

**What happened:** Something went wrong on my end. Please try again in a moment, and if the issue persists, let me know!"""
        
        return {
            "answer": friendly_message,
            "error": error_message,
            "query": query,
            "modules_used": [],
            "primary_intent": "error"
        }
    
    def format_no_intent(self, query: str) -> Dict[str, any]:
        """Format response when intent cannot be determined"""
        return {
            "answer": "I'm not sure how to help with that. Could you please rephrase your question or provide more details?",
            "query": query,
            "modules_used": [],
            "primary_intent": "unknown"
        }

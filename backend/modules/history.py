import json
import os
from typing import List, Dict
from datetime import datetime, timedelta

class HistoryManager:
    def __init__(self, file_path: str = "logs/chat_history.json"):
        self.file_path = file_path
        self._ensure_file()

    def _ensure_file(self):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_history(self) -> List[Dict]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def save_interaction(self, user_query: str, ai_response: str):
        history = self.load_history()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": "user",
            "content": user_query
        }
        history.append(entry)
        
        entry_ai = {
            "timestamp": datetime.now().isoformat(),
            "role": "assistant",
            "content": ai_response
        }
        history.append(entry_ai)
        
        # Enforce 1 week retention (optional cleanup)
        # For now, just keep last 1000 items to prevent bloat
        if len(history) > 1000:
            history = history[-1000:]
            
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2)

    def get_context_string(self, limit: int = 5) -> str:
        """Get recent conversation as a context string for LLM"""
        history = self.load_history()
        # Get last 'limit' exchanges (2 * limit items)
        recent = history[-(limit * 2):] if len(history) > 0 else []
        
        context = ""
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        return context

"""Configuration for Discord bot with Gemini API integration."""

import os
from typing import Optional


class Config:
    """Configuration class for bot tokens and settings."""
    
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant in a Discord server. 
You respond to user questions and engage in conversations naturally. 
Be friendly, concise, and helpful. When users provide context from previous messages, 
use that context to give more relevant and informed responses."""
    
    def __init__(self):
        self.discord_token: Optional[str] = os.getenv('DISCORD_TOKEN')
        self.gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')
        self.system_prompt: str = os.getenv('SYSTEM_PROMPT', self.DEFAULT_SYSTEM_PROMPT)
        
    def validate(self) -> bool:
        """Validate required environment variables are set."""
        if not self.discord_token:
            print("Error: DISCORD_TOKEN environment variable is not set")
            return False
        if not self.gemini_api_key:
            print("Error: GEMINI_API_KEY environment variable is not set")
            return False
        return True


config = Config()

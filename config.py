"""
Configuration module for Discord bot with Gemini API integration.
Loads environment variables for Discord and Gemini API tokens.
"""

import os
from typing import Optional


class Config:
    """Configuration class for bot tokens and settings."""
    
    def __init__(self):
        self.discord_token: Optional[str] = os.getenv('DISCORD_TOKEN')
        self.gemini_api_key: Optional[str] = os.getenv('GEMINI_API_KEY')
        
    def validate(self) -> bool:
        """
        Validate that all required environment variables are set.
        
        Returns:
            bool: True if all required variables are set, False otherwise.
        """
        if not self.discord_token:
            print("Error: DISCORD_TOKEN environment variable is not set")
            return False
        if not self.gemini_api_key:
            print("Error: GEMINI_API_KEY environment variable is not set")
            return False
        return True


# Global config instance
config = Config()

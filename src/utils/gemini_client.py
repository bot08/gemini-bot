"""
Gemini API client module for generating content using Google's Gemini model.
"""

import aiohttp
from typing import Optional, Dict, Any, List


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: str, system_prompt: str):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key
            system_prompt: System instruction for the AI
        """
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model = "gemini-flash-lite-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
    async def generate_content(
        self, 
        prompt: str, 
        context_messages: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Generate content using Gemini API.
        
        Args:
            prompt: The text prompt to send to Gemini
            context_messages: List of recent messages for context
            
        Returns:
            Generated text response or None if request fails
        """
        url = f"{self.base_url}?key={self.api_key}"
        
        # Build system instruction with context
        system_instruction_text = self.system_prompt
        if context_messages:
            system_instruction_text += "\n\nRecent conversation context (for reference only):\n"
            for msg in context_messages:
                system_instruction_text += f"{msg['author']}: {msg['content']}\n"
        
        # Build the contents array with the user message
        contents = [{
            "parts": [{
                "text": prompt
            }]
        }]
        
        payload = {
            "generationConfig": {
                "temperature": 0.8,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4096,
                "responseMimeType": "text/plain",
                "thinkingConfig": {
                    "thinkingBudget": 2048
                }
            },
            "system_instruction": {
                "role": "user",
                "parts": [{
                    "text": system_instruction_text
                }]
            },
            "contents": contents
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, 
                    json=payload,
                    headers={'Content-Type': 'application/json'}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._extract_text(data)
                    else:
                        error_text = await response.text()
                        print(f"Error from Gemini API: {response.status} - {error_text}")
                        return None
        except Exception as e:
            print(f"Exception while calling Gemini API: {e}")
            return None
    
    def _extract_text(self, response_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract text from Gemini API response.
        
        Args:
            response_data: JSON response from Gemini API
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            candidates = response_data.get('candidates', [])
            if candidates:
                content = candidates[0].get('content', {})
                parts = content.get('parts', [])
                if parts:
                    return parts[0].get('text', '')
            return None
        except Exception as e:
            print(f"Error extracting text from response: {e}")
            return None

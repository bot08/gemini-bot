"""
Gemini API client module for generating content using Google's Gemini model.
"""

import aiohttp
from typing import Optional, Dict, Any


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.model = "gemini-flash-lite-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
    async def generate_content(self, prompt: str) -> Optional[str]:
        """
        Generate content using Gemini API.
        
        Args:
            prompt: The text prompt to send to Gemini
            
        Returns:
            Generated text response or None if request fails
        """
        url = f"{self.base_url}?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.8,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as response:
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

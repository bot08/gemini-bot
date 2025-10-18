"""Gemini API client for content generation."""

import requests
from typing import Optional, Dict, Any, List


class GeminiClient:
    """Client for Google's Gemini API."""

    def __init__(self, api_key: str, system_prompt: str):
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.model = "gemini-flash-lite-latest"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def generate_content(self, prompt: str, context_messages: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        """Generate content using Gemini API with context."""
        # Build system instruction with context
        system_instruction_text = self.system_prompt
        if context_messages:
            system_instruction_text += "\n\nRecent conversation context (for reference only):\n"
            for msg in context_messages:
                system_instruction_text += f"{msg['author']}: {msg['content']}\n"

        payload = {
            "generationConfig": {
                "temperature": 0.7,
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
                "parts": [{"text": system_instruction_text}]
            },
            "contents": [{"parts": [{"text": prompt}]}]
        }

        try:
            response = requests.post(self.base_url, json=payload, headers={'Content-Type': 'application/json'}, timeout=60)
            if response.status_code == 200:
                return self._extract_text(response.json())
            else:
                error_data = self._parse_error(response)
                print(f"❌ Gemini API Error ({response.status_code}): {error_data}")
                return None
        except Exception as e:
            print(f"❌ Exception calling Gemini API: {e}")
            return None

    def _parse_error(self, response) -> str:
        """Parse error message from API response."""
        try:
            error_json = response.json()
            if 'error' in error_json:
                error = error_json['error']
                message = error.get('message', 'Unknown error')
                status = error.get('status', 'UNKNOWN')
                return f"{status}: {message}"
        except:
            pass
        return response.text[:200]

    def _extract_text(self, response_data: Dict[str, Any]) -> Optional[str]:
        """Extract text from API response."""
        try:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError, TypeError):
            return None

# Architecture Overview

## Project Structure

```
gemini-bot/
├── main.py                      # Application entry point
├── src/
│   ├── __init__.py
│   ├── bot/
│   │   ├── __init__.py
│   │   └── discord_bot.py      # Discord bot logic
│   └── utils/
│       ├── __init__.py
│       ├── config.py            # Configuration management
│       └── gemini_client.py    # Gemini API client
├── requirements.txt             # Python dependencies
├── Procfile                     # Heroku deployment configuration
├── runtime.txt                  # Python version specification
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
└── README.md                    # Project documentation
```

## Component Details

### main.py
Application entry point. Initializes and runs the Discord bot with proper configuration validation.

### src/bot/discord_bot.py
Main Discord bot logic. Contains:
- `GeminiBot` class that extends `discord.ext.commands.Bot`
- `on_ready()` event handler for bot initialization
- `on_message()` event handler that responds to mentions
- `get_recent_messages()` method to fetch last 10 messages for context
- Message processing logic that extracts user prompts and sends them to Gemini API
- Response handling with Discord's 2000 character limit handling

### src/utils/gemini_client.py
Handles all interactions with Google's Gemini API. Contains:
- `GeminiClient` class for API communication
- `generate_content()` async method for making API requests with context
- `_extract_text()` method for parsing API responses
- Configured with enhanced generation parameters:
  - temperature: 0.8
  - topK: 40
  - topP: 0.95
  - maxOutputTokens: 4096 (increased for longer responses)
  - thinkingBudget: 2048 (enables enhanced reasoning)
  - system_instruction: Configurable prompt with conversation context

### src/utils/config.py
Manages environment variables and configuration. Contains:
- `Config` class for loading environment variables
- `validate()` method to ensure required variables are set
- `DEFAULT_SYSTEM_PROMPT` constant with fallback system prompt
- Support for custom `SYSTEM_PROMPT` environment variable
- Global config instance for easy access across modules

## Data Flow

1. User mentions the bot in a Discord channel
2. `on_message()` handler detects the mention
3. Bot fetches last 10 messages from channel for context
4. Message content is extracted (removing mention tags)
5. System prompt is built with conversation context
6. Content and context are sent to `GeminiClient.generate_content()`
7. Gemini API processes the request with enhanced thinking capabilities
8. Response is sent back to the Discord channel
9. If response exceeds 2000 characters, it's split into multiple messages

## API Integration

### Discord API
- Uses discord.py library (version 2.3.2)
- Requires Message Content Intent enabled
- Handles async operations with proper event loop

### Gemini API
- Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent`
- Method: POST
- Authentication: API key in URL parameter
- **Note**: Using v1beta API version (beta stability level)
- Request format:
```json
{
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
      "text": "system prompt + recent message context"
    }]
  },
  "contents": [{
    "parts": [{"text": "user prompt"}]
  }]
}
```

## Deployment

### Heroku Configuration
- **Procfile**: Specifies `worker` dyno running `python bot.py`
- **runtime.txt**: Specifies Python 3.11.7
- **Environment Variables**: Set via Heroku config vars

### Required Environment Variables
- `DISCORD_TOKEN`: Bot authentication token from Discord Developer Portal
- `GEMINI_API_KEY`: API key from Google AI Studio
- `SYSTEM_PROMPT`: (Optional) Custom system prompt for the AI assistant

## Error Handling

- Invalid API responses are caught and logged
- Discord API errors are handled by discord.py
- Configuration validation prevents startup with missing variables
- Network errors during API calls result in user-friendly error messages

## Security Considerations

- Tokens stored as environment variables (never in code)
- .gitignore prevents accidental token commits
- API keys not exposed in logs or error messages
- Bot only responds to mentions (prevents spam)

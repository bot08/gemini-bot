# Architecture Overview

## Project Structure

```
gemini-bot/
├── bot.py              # Main Discord bot application
├── gemini_client.py    # Gemini API client
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── Procfile           # Heroku deployment configuration
├── runtime.txt        # Python version specification
├── .env.example       # Example environment variables
├── .gitignore         # Git ignore rules
└── README.md          # Project documentation
```

## Component Details

### bot.py
Main entry point for the Discord bot. Contains:
- `GeminiBot` class that extends `discord.ext.commands.Bot`
- `on_ready()` event handler for bot initialization
- `on_message()` event handler that responds to mentions
- Message processing logic that extracts user prompts and sends them to Gemini API
- Response handling with Discord's 2000 character limit handling

### gemini_client.py
Handles all interactions with Google's Gemini API. Contains:
- `GeminiClient` class for API communication
- `generate_content()` async method for making API requests
- `_extract_text()` method for parsing API responses
- Configured with generation parameters:
  - temperature: 0.8
  - topK: 40
  - topP: 0.95
  - maxOutputTokens: 1024

### config.py
Manages environment variables and configuration. Contains:
- `Config` class for loading environment variables
- `validate()` method to ensure required variables are set
- Global config instance for easy access across modules

## Data Flow

1. User mentions the bot in a Discord channel
2. `on_message()` handler detects the mention
3. Message content is extracted (removing mention tags)
4. Content is sent to `GeminiClient.generate_content()`
5. Gemini API processes the request and returns a response
6. Response is sent back to the Discord channel
7. If response exceeds 2000 characters, it's split into multiple messages

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
  "contents": [{
    "parts": [{"text": "user prompt"}]
  }],
  "generationConfig": {
    "temperature": 0.8,
    "topK": 40,
    "topP": 0.95,
    "maxOutputTokens": 1024
  }
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

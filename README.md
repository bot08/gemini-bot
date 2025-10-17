# Gemini Discord Bot

Discord bot that integrates with Google's Gemini API to generate AI-powered responses when mentioned.

## Features

- Responds to @mentions with AI-generated content
- Uses Google's Gemini Flash Lite model
- Configurable generation parameters (temperature, topK, topP)
- Ready for Heroku deployment

## Architecture

The bot follows a modular structure organized in folders:

```
gemini-bot/
├── main.py                      # Entry point
├── src/
│   ├── bot/
│   │   └── discord_bot.py      # Discord bot logic and event handlers
│   └── utils/
│       ├── config.py            # Configuration management
│       └── gemini_client.py    # Gemini API client
```

Key features:
- **Message Context**: Bot fetches last 10 messages for better context-aware responses
- **System Prompt**: Configurable via SYSTEM_PROMPT environment variable
- **Enhanced API**: Uses Gemini's thinking config for improved responses

## Prerequisites

- Python 3.11+
- Discord Bot Token
- Google Gemini API Key

## Setup

### 1. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Enable "Message Content Intent" in the bot settings
5. Copy the bot token

### 2. Gemini API Setup

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 3. Local Development

1. Clone the repository:
```bash
git clone https://github.com/bot08/gemini-bot.git
cd gemini-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your tokens:
```env
DISCORD_TOKEN=your_discord_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

4. Run the bot:
```bash
python main.py
```

Note: For local development with `.env` file, install python-dotenv:
```bash
pip install python-dotenv
```

And add this to the top of `src/utils/config.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### 4. Heroku Deployment

1. Create a new Heroku app:
```bash
heroku create your-app-name
```

2. Set environment variables:
```bash
heroku config:set DISCORD_TOKEN=your_discord_bot_token
heroku config:set GEMINI_API_KEY=your_gemini_api_key
```

3. Deploy to Heroku:
```bash
git push heroku main
```

4. Scale the worker dyno:
```bash
heroku ps:scale worker=1
```

## Usage

1. Invite the bot to your Discord server using the OAuth2 URL from the Discord Developer Portal
2. Mention the bot in a channel with your message: `@YourBot What is the weather like?`
3. The bot will respond with AI-generated content from Gemini

## Configuration

The Gemini API is configured with the following parameters in `src/utils/gemini_client.py`:

- **Model**: `gemini-flash-lite-latest`
- **Temperature**: 0.8 (controls randomness)
- **TopK**: 40 (limits vocabulary to top K tokens)
- **TopP**: 0.95 (nucleus sampling threshold)
- **MaxOutputTokens**: 4096 (maximum response length)
- **ThinkingBudget**: 2048 (enhanced reasoning capability)
- **System Instruction**: Configurable system prompt with conversation context

The bot automatically includes the last 10 messages from the channel as context in each request, allowing for more contextual and relevant responses.

You can adjust these values in the `generate_content` method.

## Environment Variables

- `DISCORD_TOKEN` - Your Discord bot token (required)
- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `SYSTEM_PROMPT` - Custom system prompt for the AI (optional, has sensible default)

## License

MIT
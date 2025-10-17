"""Main entry point for the Gemini Discord Bot."""

from dotenv import load_dotenv
load_dotenv()
from src.utils.config import config
from src.bot.discord_bot import GeminiBot


def main():
    if not config.validate():
        print("Configuration validation failed. Exiting.")
        return
    
    bot = GeminiBot()
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()

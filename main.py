"""
Main entry point for the Gemini Discord Bot.
"""

from src.utils.config import config
from src.bot.discord_bot import GeminiBot


def main():
    """Main function to run the bot."""
    # Validate configuration
    if not config.validate():
        print("Configuration validation failed. Exiting.")
        return
    
    # Create and run bot
    bot = GeminiBot()
    bot.run(config.discord_token)


if __name__ == "__main__":
    main()

"""
Discord bot that responds to mentions with Gemini API-generated content.
"""

import discord
from discord.ext import commands
from config import config
from gemini_client import GeminiClient


class GeminiBot(commands.Bot):
    """Discord bot with Gemini API integration."""
    
    def __init__(self):
        """Initialize the bot with proper intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents)
        self.gemini_client = GeminiClient(config.gemini_api_key)
    
    async def setup_hook(self):
        """Called when the bot is starting up."""
        print(f"Bot is starting up...")
    
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("Bot is ready!")
    
    async def on_message(self, message: discord.Message):
        """
        Handle incoming messages.
        
        Args:
            message: Discord message object
        """
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        # Check if the bot is mentioned
        if self.user in message.mentions:
            # Extract the message content without the mention
            content = message.content
            for mention in message.mentions:
                content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            content = content.strip()
            
            # If there's no content after removing mentions, provide a default prompt
            if not content:
                content = "Hello! How can I help you?"
            
            # Show typing indicator while processing
            async with message.channel.typing():
                # Call Gemini API
                response = await self.gemini_client.generate_content(content)
                
                if response:
                    # Discord has a 2000 character limit per message
                    if len(response) > 2000:
                        # Split into chunks if response is too long
                        chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                        for chunk in chunks:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(response)
                else:
                    await message.channel.send("Sorry, I couldn't generate a response. Please try again later.")
        
        # Process commands if any
        await self.process_commands(message)


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

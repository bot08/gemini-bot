"""Discord bot with Gemini API integration."""

import discord
from discord.ext import commands
from typing import List, Dict
from src.utils.config import config
from src.utils.gemini_client import GeminiClient


class GeminiBot(commands.Bot):
    """Discord bot with Gemini API integration."""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents)
        self.gemini_client = GeminiClient(config.gemini_api_key, config.system_prompt)
    
    async def setup_hook(self):
        print(f"Bot is starting up...")
    
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("Bot is ready!")
    
    async def get_recent_messages(self, channel: discord.TextChannel, limit: int = 12) -> List[Dict[str, str]]:
        """Fetch recent messages from channel for context."""
        messages = []
        try:
            async for message in channel.history(limit=limit):
                if not message.content:
                    continue
                
                content = message.content
                for mention in message.mentions:
                    content = content.replace(f'<@{mention.id}>', f'@{mention.display_name}')
                    content = content.replace(f'<@!{mention.id}>', f'@{mention.display_name}')
                
                messages.append({
                    'author': message.author.display_name,
                    'content': content.strip()
                })
            
            messages.reverse()
        except Exception as e:
            print(f"Error fetching message history: {e}")
        
        return messages
    
    async def on_message(self, message: discord.Message):
        """Handle incoming messages."""
        if message.author == self.user:
            return
        
        if self.user in message.mentions:
            content = message.content
            for mention in message.mentions:
                content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            content = content.strip()
            
            if not content:
                content = "Hello! How can I help you?"
            
            async with message.channel.typing():
                context_messages = await self.get_recent_messages(message.channel, limit=10)
                response = self.gemini_client.generate_content(content, context_messages)
                
                if response:
                    if len(response) > 2000:
                        chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
                        for chunk in chunks:
                            await message.channel.send(chunk)
                    else:
                        await message.channel.send(response)
                else:
                    await message.channel.send("Sorry, I couldn't generate a response. Please try again later.")
        
        await self.process_commands(message)

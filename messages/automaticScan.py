import discord
from discord.ext import commands
from utils.functions.extractUrls import extract_urls
from utils.functions.scanUrls import scan_urls

# Cog modularization for AutomaticScans
class AutomaticScans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return # Ignore messages sent by the bot
        
        if message.content.startswith('#'):
            return # Ignore message sent with prefix #
        
        # filters urls from message content
        urls = extract_urls(message.content)
        if urls:
            await handle_urls(message, urls)

async def handle_urls(message: discord.Message, urls: list[str]):
        try:
            await message.add_reaction('🔍')
            results = await scan_urls(urls)
            await message.clear_reaction('🔍')
            for result in results:
                if result['status'] == 'clean':
                    await message.add_reaction('✅')
                else:
                    await message.add_reaction('❗')
                    await message.channel.send(result['message'])
        except Exception as error:  
            await message.clear_reactions()
            await message.add_reaction('❓')
            print(error)
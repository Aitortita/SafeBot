import discord
from discord.ext import commands
import asyncio
from utils.functions.extractUrls import extract_urls
from utils.functions.scanUrl import scan_url

clean: str = 'clean'

# Cog modularization for discord.py
class automaticScans(commands.Cog):
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
                if result['status'] == clean:
                    await message.add_reaction('✅')
                else:
                    await message.add_reaction('❗')
                    await message.channel.send(result['message'])
        except Exception as error:
            await message.clear_reactions()
            await message.add_reaction('❓')
            print(error)

# automatic scan function using requests on virus total api
async def scan_urls(urls: list[str]) -> list[dict]:
    """
  This function scans a list of URLs and returns the results.

  Args:
    urls: A list of URLs to scan.

  Returns:
    A list of dict containing the results of the scan.
    """
    # Create a list of asynchronous scans to scan each URL.
    scans = [scan_url(url) for url in urls]

    # Start all of the scans at the same time and wait for them to complete.
    results = await asyncio.gather(*scans)

    return results

async def setup(bot: commands.Bot):
    await bot.add_cog(automaticScans(bot))
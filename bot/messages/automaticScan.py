import discord
from discord.ext import commands
from utils.functions import extract_urls, scan_urls, extractDomainsFromUrls, extractDomain
from database.queries import checkIfSafeDomain

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
        
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            # Message was sent via DM or group DM channel
            urls = extract_urls(message.content)
            if urls:
                await handle_urls_on_DM(message, urls)
            return
        
        # filters urls from message content
        urls = extract_urls(message.content)
        if (not urls):
            return
        domains = extractDomainsFromUrls(urls)
        unsafe_domains = await checkIfSafeDomain(message.guild.id, domains)
        if (not unsafe_domains):
            return
        filtered_urls = [url for url in urls if extractDomain(url) in unsafe_domains]
        if filtered_urls:
            print(f"filtered_urls: {filtered_urls}")
            await handle_urls(message, filtered_urls)

async def handle_urls_on_DM(message: discord.Message, urls: list[str]):
        try:
            results = await scan_urls(urls)
            for result in results:
                if result['status'] == 'clean':
                    await message.add_reaction('✅')
                    await message.channel.send(result['message'])
                else:
                    await message.add_reaction('❗')
                    await message.channel.send(result['message'])
        except Exception as error:  
            await message.add_reaction('❓')
            await message.channel.send("There was an error scanning your link, try again")
            print(error)

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
import discord
from discord.ext import commands
from utils.functions import extract_urls, scan_urls, extractDomainsFromUrls, extractDomain, scan_files
from database.queries import checkIfWhitelistedDomain

# Cog modularization for AutomaticScans
class AutomaticScans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        # Check if message was sent via DM or group DM channel
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            urls = extract_urls(message.content)
            if urls:
                await handle_urls_on_message(message, urls, self.bot.user)
            return

        if (message.attachments):
            await handle_files_on_message(message, self.bot.user)

        # filters urls from message content
        urls = extract_urls(message.content)
        if (urls):
            domains = extractDomainsFromUrls(urls)
            unsafe_domains = await checkIfWhitelistedDomain(message.guild.id, domains)
            if (unsafe_domains):
                filtered_urls = [url for url in urls if extractDomain(url) in unsafe_domains]
                if filtered_urls:
                    await handle_urls_on_message(message, filtered_urls, self.bot.user)

async def handle_files_on_message(message: discord.Message, bot_user):
    try:
        await message.add_reaction('🔍')
        results = await scan_files(message.attachments)
        await message.remove_reaction('🔍', bot_user)
        for result in results:
            if result['status'] == 'clean':
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❗')
                await message.channel.send(result['message'])
    except Exception as error:
        await message.add_reaction('❓')
        await message.channel.send("There was an error scanning your file, try again later")
        print(error)

async def handle_urls_on_message(message: discord.Message, urls: list[str], bot_user: str):
    try:
        await message.add_reaction('🔍')
        results = await scan_urls(urls)
        await message.remove_reaction('🔍', bot_user)
        for result in results:
            if result['status'] == 'clean':
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❗')
                await message.channel.send(result['message'])
    except Exception as error:
        await message.add_reaction('❓')
        await message.channel.send("There was an error scanning your link, try again later")
        print(error)
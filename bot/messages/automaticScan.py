import discord
from discord.ext import commands
from utils.functions import extract_urls, extract_domains_from_urls, extract_domain, handle_urls_on_message, handle_files_on_message, handle_files_on_dm, handle_urls_on_dm
from database.queries import checkIfWhitelistedDomain
from logging import getLogger
bot = getLogger("bot")

# Cog modularization for AutomaticScans
class AutomaticScans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        # filters urls from message content
        urls = extract_urls(message.content)

        # Check if message was sent via DM or group DM channel
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.GroupChannel):
            if message.attachments:
                await handle_files_on_dm(message, urls, self.bot.user)
            if urls:
                await handle_urls_on_dm(message, urls, self.bot.user)
            return

        if message.attachments:
            await handle_files_on_message(message, self.bot.user)

        if urls:
            domains = extract_domains_from_urls(urls)
            unsafe_domains = await checkIfWhitelistedDomain(message.guild.id, domains)
            if unsafe_domains:
                filtered_urls = [url for url in urls if extract_domain(url) in unsafe_domains]
                if filtered_urls:
                    await handle_urls_on_message(message, filtered_urls, self.bot.user)

    @commands.Cog.listener()
    async def on_message_edit(self, old_message: discord.Message, new_message: discord.Message):
        # Ignore messages sent by the bot
        if new_message.author == self.bot.user:
            return

        # filters urls from message content
        urls = extract_urls(new_message.content)

        # Check if message was sent via DM or group DM channel
        if isinstance(new_message.channel, discord.DMChannel) or isinstance(new_message.channel, discord.GroupChannel):
            if new_message.attachments:
                await handle_files_on_dm(new_message, urls, self.bot.user)
            if urls:
                await handle_urls_on_dm(new_message, urls, self.bot.user)
            return

        if new_message.attachments:
            await handle_files_on_message(new_message, self.bot.user)

        if urls:
            domains = extract_domains_from_urls(urls)
            unsafe_domains = await checkIfWhitelistedDomain(new_message.guild.id, domains)
            if unsafe_domains:
                filtered_urls = [url for url in urls if extract_domain(url) in unsafe_domains]
                if filtered_urls:
                    await handle_urls_on_message(new_message, filtered_urls, self.bot.user)
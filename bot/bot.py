from logging import getLogger
import config.settings as settings
import discord
from discord.ext import commands
from bot.commands import NormalCommands, ScanCommands
from bot.messages import AutomaticScans
logger = getLogger("bot")

intents = discord.Intents.default()  # Create a default intents instance
intents.typing = False  # Disable the typing event
intents.presences = False  # Disable presence-related events
intents.message_content = True

command_prefix = ">"

class SafeBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def on_ready(self):
        logger.info(f"Bot: {self.user} (ID: {self.user.id}) is now running")
        await self.change_presence(status=discord.Status.idle, activity=discord.Game("Protecting you"))

        # Add cogs and await the add_cog methods
        await self.add_cog(NormalCommands(self))
        await self.add_cog(ScanCommands(self))
        await self.add_cog(AutomaticScans(self))
        await self.tree.sync()

    def run_bot(self):
        self.run(settings.DISCORD_API_TOKEN, root_logger=True)
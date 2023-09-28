from logging import getLogger
import settings
import discord
from discord.ext import commands
from commands.NormalCommands import NormalCommands
from messages.automaticScan import AutomaticScans
from commands.ScanCommands import ScanCommands
logger = getLogger("bot")

intents = discord.Intents.default()  # Create a default intents instance
intents.typing = False  # Disable the typing event
intents.presences = False  # Disable presence-related events
intents.message_content = True

bot = commands.Bot(command_prefix=("#"), intents=intents)

def run_discord_bot():
    @bot.event
    async def on_ready():
        logger.info(f"Bot: {bot.user} (ID: {bot.user.id}) is now running")
        # Set bot status
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game("Protecting you"))

        await bot.add_cog(NormalCommands(bot))
        await bot.add_cog(ScanCommands(bot))
        await bot.add_cog(AutomaticScans(bot))
        await bot.tree.sync()
                
    bot.run(settings.DISCORD_API_TOKEN, root_logger=True)
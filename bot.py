import settings
import discord
from discord.ext import commands
from logging import getLogger

logger = getLogger("bot")

intents = discord.Intents.default()  # Create a default intents instance
intents.typing = False  # Disable the typing event
intents.presences = False  # Disable presence-related events
intents.message_content = True

async def get_prefix(bot: commands.Bot, message: discord.Message):
    return '#'

def run_discord_bot():

    bot = commands.Bot(command_prefix=(get_prefix), intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f"Bot: {bot.user} (ID: {bot.user.id}) is now running")

        # Set bot status
        game = discord.Game("Protecting you")
        await bot.change_presence(status=discord.Status.idle, activity=game)

        # import modularized Cogs
        for message_file in settings.MESSAGES_DIR.glob("*.py"):
            if message_file.name != "__init__.py":
                await bot.load_extension(f"messages.{message_file.name[:-3]}")

    @bot.event
    async def on_command_error(ctx: commands.Context, error):
         if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument", ephemeral=True)

    class InviteButtons(discord.ui.View):
            def __init__(self, inv: str):
                super().__init__()
                self.inv = inv
                self.add_item(discord.ui.Button(label="Invite Link", url=self.inv))

            @discord.ui.button(label="Invite Btn", style=discord.ButtonStyle.blurple)
            async def inviteBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
                await interaction.response.send_message(self.inv, ephemeral=True)

    @bot.command()
    async def invite(ctx: commands.Context):
        inv = "https://discord.gg/5fpCmgRGV2"
        await ctx.send("Click the buttons below to invite someone!", view=InviteButtons(str(inv)))

    @bot.command()
    async def ping(ctx: commands.Context):
        await ctx.send("pong")

    bot.run(settings.DISCORD_API_TOKEN, root_logger=True)
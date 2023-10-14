import discord
from discord.ext import commands
from discord import app_commands
from database.queries import addSafeDomain

# Cog modularization for NormalCommands 
class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__cog_name__= "Config commands"

    @commands.hybrid_command(
    description="Adds a domain to the list of domains to ignore",
    with_app_command=True
    )
    @app_commands.describe(text_to_send="example.com")
    @app_commands.rename(text_to_send="domain_to_add")
    async def add_safe_domain(self, ctx: commands.Context, text_to_send: str):
        result = await addSafeDomain(ctx.guild.id, text_to_send)
        if result:
            await ctx.send(f"the domain '{result}' was added successfully to your safe domains, this means we will now ignore this domain with our automatic scans")
        else:
            await ctx.send("An error ocurred, we recommend sending this to support at our discord")
            
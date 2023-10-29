import discord
from discord.ext import commands
from discord import app_commands
from database.queries import addWhitelistedDomain, getWhitelist

# Cog modularization for NormalCommands 
class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__cog_name__= "Config commands"

    @commands.hybrid_command(
        description="Adds a domain to the whitelist, ensuring it won't be scanned automatically.",
        with_app_command=True
    )
    @app_commands.describe(text_to_send="example.com")
    @app_commands.rename(text_to_send="domain_to_add")
    async def whitelist_domain(self, ctx: commands.Context, text_to_send: str):
        """Adds a domain to the whitelist, ensuring it won't be scanned automatically."""
        result = await addWhitelistedDomain(ctx.guild.id, text_to_send)
        if result:
            await ctx.send(result)
        else:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")

    @commands.hybrid_command(
        description= "",
        with_app_command=True
    )
    async def show_whitelist(self, ctx: commands.Context):
        """ Shows the whitelisted domains on the server."""
        result = await getWhitelist(ctx.guild.id)
        result = ', '.join(f"'{domain}'" for domain in result)
        await ctx.send(result)
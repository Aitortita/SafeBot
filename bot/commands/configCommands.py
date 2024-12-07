from discord.ext import commands
from discord import app_commands
from database.queries import addWhitelistedDomain, getWhitelist, deleteWhitelistedDomain, turn_on_quiet_mode, turn_off_quiet_mode, check_if_quiet_mode
from logging import getLogger
bot = getLogger("bot")

class ConfigCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__cog_name__= "Config commands"

    @commands.hybrid_command(
        description= "Shows the whitelisted domains on the server.",
        with_app_command=True
    )
    async def show_whitelist(self, ctx: commands.Context):
        """Shows the whitelisted domains on the server."""
        try:
            result = await getWhitelist(ctx.guild.id)
            result = ', '.join(f"'{domain}'" for domain in result)
            await ctx.send(result)
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)

    @commands.hybrid_command(
        description="Adds a domain to the whitelist, ensuring it won't be scanned automatically.",
        with_app_command=True
    )
    @app_commands.describe(text_to_send="example.com")
    @app_commands.rename(text_to_send="domain_to_add")
    async def whitelist_domain(self, ctx: commands.Context, text_to_send: str):
        """Adds a domain to the whitelist, ensuring it won't be scanned automatically."""
        try:
            result = await addWhitelistedDomain(ctx.guild.id, text_to_send)
            if result:
                await ctx.send(result)
            else:
                await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)

    @commands.hybrid_command(
        description="Deletes a domain from the whitelist, meaning it will be scanned automatically again.",
        with_app_command=True
    )
    @app_commands.describe(text_to_send="example.com")
    @app_commands.rename(text_to_send="domain_to_delete")
    async def unwhitelist_domain(self, ctx: commands.Context, text_to_send: str):
        """Deletes a domain from the whitelist, meaning it will be scanned automatically again."""
        try:
            result = await deleteWhitelistedDomain(ctx.guild.id, text_to_send)
            if result:
                await ctx.send(result)
            else:
                await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)

    @commands.hybrid_command(
        description="""The bot will only react when the result is malicious or there is an error while scanning""",
        with_app_command=True
    )
    async def quiet_mode_on(self, ctx: commands.Context):
        """Turns on the quiet mode."""
        try:
            result = await turn_on_quiet_mode(ctx.guild.id)
            if result == True:
                await ctx.send("Quiet mode is now on")
            else:
                await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)

    @commands.hybrid_command(
        description="The bot will react to everything to tell users it's analizing",
        with_app_command=True
    )
    async def quiet_mode_off(self, ctx: commands.Context):
        """Turns off the quiet mode."""
        try:
            result = await turn_off_quiet_mode(ctx.guild.id)
            if result == False:
                await ctx.send("Quiet mode is now off")
            else:
                await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)

    @commands.hybrid_command(
        description="The bot will react to everything to tell users it's analizing",
        with_app_command=True
    )
    async def status(self, ctx: commands.Context):
        """Gives status info of the bot on the server."""
        try:
            result = await check_if_quiet_mode(ctx.guild.id)
            await ctx.send(f"Quiet mode is {'on' if result == True else 'off'}")
        except Exception as error:
            await ctx.send("An error ocurred, we recommend sending this to the support at our discord which you can find by running /invite")
            bot.error(error)
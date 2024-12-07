from discord.ext import commands
from discord import app_commands

class ScanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__cog_name__= "Scan commands"
        self.description = "Commands to scan domains, urls and files"

    @commands.hybrid_command(
            description="Scans a domain and shows a full analysis",
            with_app_command=True
            )
    @app_commands.describe(text_to_send="example.com")
    @app_commands.rename(text_to_send="domain_to_scan")
    async def scan_domain(self, ctx: commands.Context, text_to_send: str):
        ''' Scans a domain and gives a full report regardless of it's outcome '''
        await ctx.send(f"be right back, we are fighting '{text_to_send}'")

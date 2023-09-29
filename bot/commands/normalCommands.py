import discord
from discord.ext import commands

class InviteButtons(discord.ui.View):
        def __init__(self, inv: str):
            super().__init__()
            self.inv = inv
            self.add_item(discord.ui.Button(label="Invite Link", url=self.inv))

        @discord.ui.button(label="Invite Btn", style=discord.ButtonStyle.blurple)
        async def inviteBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(self.inv, ephemeral=True)

# Cog modularization for NormalCommands 
class NormalCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.__cog_name__= "Normal commands"

    @commands.hybrid_command()
    async def invite(self, ctx: commands.Context):
        """Gives you an invite to Safebot's discord."""
        inv = "https://discord.gg/5fpCmgRGV2"
        await ctx.send("Click the buttons below to invite someone!", view=InviteButtons(str(inv)))

    @commands.hybrid_command()
    async def ping(self, ctx: commands.Context):
        """Answers with 'pong'."""
        await ctx.send("pong")
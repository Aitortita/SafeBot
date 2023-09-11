import settings
import re
import vt
import json
import discord
from discord.ext import commands
from utils.vtScanResponseInterface import Response

client = vt.Client(settings.VIRUSTOTAL_API_KEY)

class automaticScans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.check(lambda message: not message.content.startswith('#'))
    async def on_message(self, message):
        if message.author == self.bot.user:
            return # Ignore messages sent by the bot
        
        user_name = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        discord_name = str(message.guild)
        print(f"{user_name} said: '{user_message}' ({channel}-{discord_name})")
        
        if isinstance(message.channel, discord.DMChannel):
            return await send_message(message, user_message, is_private=True)
        await send_message(message, user_message, is_private=False)

async def send_message(message, user_message, is_private):
        try:
            response = await handle_response(user_message, is_private)
            if not response:
                return
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as error:
            print(f"error: ${error}")

# function to extract urls from user's messages
def extract_urls(message):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    urls = url_pattern.findall(message)
    return urls

# main response function
async def handle_response(user_message: str, is_private: bool) -> str:
    p_message = user_message
    urls = extract_urls(p_message)

    if urls:
        try:
            url_id = vt.url_id(urls[0])
            response: Response = await client.get_object_async("/urls/{}", url_id)
            print(response.reputation)
        except Exception as error:
            print(f"An unexpected error occurred: {str(error)}")
            return(f"An unexpected error occurred: {str(error)}")
    
    if p_message == 'hello':
        return 'Hey there!'

    if p_message == 'help' and is_private:
        return "`This is a help message that you can modify.`"
    
    return

async def setup(bot):
    await bot.add_cog(automaticScans(bot))
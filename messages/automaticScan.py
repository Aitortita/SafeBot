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
            antivirusFlags = {}
            url_id = vt.url_id(urls[0])
            response: Response = await client.get_object_async("/urls/{}", url_id)
            for antivirus, detection_result in response.last_analysis_results.items():
                 if detection_result["result"] == "phishing" or detection_result["result"] == "malicious":
                    antivirusFlags[antivirus] = detection_result["result"]
            if len(antivirusFlags) >= 1:
                return (f"the url {response.last_final_url} is malicious, don't click it.\nHere is a list of the antivirus that listed it as malicious: ```json\n{json.dumps(antivirusFlags, indent=3)}\n```")
        except Exception as error:
            print(error)

    return

async def setup(bot):
    await bot.add_cog(automaticScans(bot))
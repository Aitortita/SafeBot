import settings
import json
import discord
import requests
import time
from discord.ext import commands
from utils.functions.extractUrls import extract_urls
from utils.functions.urlIdGenerator import url_id_generator

headers = {
    "accept": "application/json",
    "X-Apikey": settings.VIRUSTOTAL_API_KEY
}

malicious: str = 'malicious'
clean: str = 'clean'
queued: str = 'queued'

# Cog modularization for discord.py
class automaticScans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return # Ignore messages sent by the bot
        if message.content.startswith('#'):
            return # Ignore message sent with prefix #
        # filters urls from message content
        urls = extract_urls(message.content)
        if urls:
            await handle_urls(message, urls)

async def handle_urls(message: discord.Message, urls):
        try:
            await message.add_reaction('🔍')
            results = await urlScan(urls)
            await message.clear_reaction('🔍')
            if results['status'] == clean:
                await message.add_reaction('✅')
            if results['status'] == malicious:
                await message.add_reaction('❗')
                await message.channel.send(results['message'])
        except Exception as error:
            await message.clear_reactions()
            await message.add_reaction('❓')
            print(error)

# automatic scan function using requests on virus total api
async def urlScan(urls: list) -> dict:
    """
  This function scans a list of URLs and returns the results.o

  Args:
    urls: A list of URLs to scan.

  Returns:
    A Dict containing the results of the scan.
  """
    url_ids = url_id_generator(urls)
    # print(url_ids)
    antivirusFlags = {}
    # async with requests.Session() as session:
    #         for url_id in url_ids:
    try:
        response = requests.get(f"https://www.virustotal.com/api/v3/urls/{url_ids[0]}", headers=headers)
        if(response.status_code == 200):
            analysis = requests.post(f"https://www.virustotal.com/api/v3/urls/{url_ids[0]}/analyse", headers=headers)
            if (analysis.status_code == 200):
                response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis.json()['data']['id']}", headers=headers)
                while response.json()['data']['attributes']['status'] == "queued":
                    time.sleep(2)
                    response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis.json()['data']['id']}", headers=headers)
                for antivirus, detection_result in response.json()['data']['attributes']['results'].items():
                    if detection_result["result"] == "phishing" or detection_result["result"] == "malicious":
                        antivirusFlags[antivirus] = detection_result["result"]
                if len(antivirusFlags) >= 1:
                    return {
                        'status': malicious,
                        'message': f"the url '{response.json()['meta']['url_info']['url']}' is malicious, don't click it.\nHere is a list of the antivirus that listed it as malicious: ```json\n{json.dumps(antivirusFlags, indent=3)}\n```"
                    }
                return {
                    'status': clean
                }
        else:
            analysis = requests.post("https://www.virustotal.com/api/v3/urls", data={ "url": urls[0] }, headers={
                "accept": "application/json",
                "X-Apikey": settings.VIRUSTOTAL_API_KEY,
                "content-type": "application/x-www-form-urlencoded"
            })
            if(analysis.status_code == 200):
                response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis.json()['data']['id']}", headers=headers)
                while response.json()['data']['attributes']['status'] == "queued":
                    time.sleep(2)
                    response = requests.get(f"https://www.virustotal.com/api/v3/analyses/{response.json()['data']['id']}", headers=headers)
                for antivirus, detection_result in response.json()['data']['attributes']['results'].items():
                    if detection_result["result"] == "phishing" or detection_result["result"] == "malicious":
                        antivirusFlags[antivirus] = detection_result["result"]
                if len(antivirusFlags) >= 1:
                    return {
                        'status': malicious,
                        'message': f"the url '{response.json()['meta']['url_info']['url']}' is malicious, don't click it.\nHere is a list of the antivirus that listed it as malicious: ```json\n{json.dumps(antivirusFlags, indent=3)}\n```"
                    }
                return {
                    'status': clean
                }
    except Exception as error:
        print(error)

async def setup(bot: commands.Bot):
    await bot.add_cog(automaticScans(bot))
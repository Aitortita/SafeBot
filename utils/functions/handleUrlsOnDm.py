import discord
from .scanUrls import scan_urls
from logging import getLogger
bot = getLogger("bot")

async def handle_urls_on_dm(message: discord.Message, urls: list[str], bot_user: str):
    try:
        await message.add_reaction('🔍')
        results = await scan_urls(urls)
        await message.remove_reaction('🔍', bot_user)
        for result in results:
            if result['status'] == 'clean':
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❗')
                await message.channel.send(result['message'])
    except Exception as error:
        await message.add_reaction('❓')
        await message.channel.send("There was an error scanning your link, try again later")
        bot.info(error)
import discord
from .scanUrls import scan_urls
from database.queries import check_if_quiet_mode
from logging import getLogger
bot = getLogger("bot")

async def handle_urls_on_message(message: discord.Message, urls: list[str], bot_user: str):
    try:
        quietMode : bool = await check_if_quiet_mode(message.guild.id)
        if quietMode:
            results = await scan_urls(urls)
            for result in results:
                if result['status'] != 'clean':
                    await message.add_reaction('❗')
                    await message.channel.send(result['message'])
        else:
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
        bot.info(error)

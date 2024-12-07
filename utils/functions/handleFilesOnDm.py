import discord
from .scanFiles import scan_files
from logging import getLogger
bot = getLogger("bot")

async def handle_files_on_dm(message: discord.Message, bot_user):
    try:
        await message.add_reaction('🔍')
        results = await scan_files(message.attachments)
        await message.remove_reaction('🔍', bot_user)
        for result in results:
            if result['status'] == 'clean':
                await message.add_reaction('✅')
            else:
                await message.add_reaction('❗')
                await message.channel.send(result['message'])
    except Exception as error:
        await message.add_reaction('❓')
        await message.channel.send("There was an error scanning your file, try again later")
        bot.info(error)
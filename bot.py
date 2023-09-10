import discord
import responses
import os

async def send_message(message, user_message, is_private):
        response = await responses.handle_response(user_message, is_private)
        if not response:
            return
        await message.author.send(response) if is_private else await message.channel.send(response)

def run_discord_bot():
    TOKEN = os.getenv('TOKEN')
    intents = discord.Intents.default()  # Create a default intents instance
    intents.typing = False  # Disable the typing event
    intents.presences = False  # Disable presence-related events
    intents.message_content = True

    client = discord.Client(intents=intents)  # Pass the intents when creating the client

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
        # Set bot status
        game = discord.Game("Protecting you")
        await client.change_presence(status=discord.Status.idle, activity=game)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return # Ignore messages sent by the bot
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if isinstance(message.channel, discord.DMChannel):
            return await send_message(message, user_message, is_private=True)

        if user_message[0] == '#':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
from dotenv import load_dotenv
import bot
import os

def configure():
        load_dotenv()

def main():
    configure()
    print(os.getenv("TOKEN"))
    bot.run_discord_bot()

main()
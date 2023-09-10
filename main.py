from dotenv import load_dotenv
import bot

def configure():
        load_dotenv()

def main():
    configure()
    bot.run_discord_bot()

main()
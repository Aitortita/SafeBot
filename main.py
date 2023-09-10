from dotenv import load_dotenv
import bot
import os

def configure():
        try:
            load_dotenv()
        except:
            print("MAN Test failed")

def main():
    configure()
    print(os.getenv("TOKEN"))
    bot.run_discord_bot()

main()
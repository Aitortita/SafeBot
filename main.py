from bot import SafeBot
import database

if __name__ == '__main__':
    try:
        # Create bot instance
        bot = SafeBot()
        bot.run_bot()
    except Exception as error:
        print(error)
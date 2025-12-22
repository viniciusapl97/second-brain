from dotenv import load_dotenv
load_dotenv()  # 🔴 ESSENCIAL: carrega o .env antes de qualquer import

from app.bot.telegram_bot import run_bot

if __name__ == "__main__":
    run_bot()

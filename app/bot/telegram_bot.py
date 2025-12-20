import os
import logging
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    filters,
)
from app.ai.intent_router import IntentRouter
from app.bot.messages import GENERAL_START
from app.bot.handlers.memory.memory_handler import (
    handle_memory_text,
    handle_memory_confirmation,
)
from app.bot.handlers.help_handler import handle_help
from app.bot.handlers.memory.memory_list_handler import handle_list_memories

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

load_dotenv()

router = IntentRouter()


async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    decision = router.route(text)

    if decision["intent"] == "memory":
        await handle_memory_text(update, context)

    elif decision["intent"] == "finance":
        # por enquanto, só feedback
        await update.message.reply_text(
            "Módulo financeiro em construção."
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        GENERAL_START,
        parse_mode="Markdown"
    )


async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_memory_text(update, context)


def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    app = ApplicationBuilder().token(token).build()

    # 🔹 CONFIRMAÇÃO DE MEMÓRIA
    app.add_handler(
        CallbackQueryHandler(
            handle_memory_confirmation,
            pattern=r"^memory:(confirm|cancel)$"
        )
    )

    # 🔹 COMANDOS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", handle_help))
    app.add_handler(CommandHandler("ultimas", handle_list_memories))

    # 🔹 TEXTO LIVRE
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, route_message)
    )

    print("Telegram bot is running...")
    app.run_polling()

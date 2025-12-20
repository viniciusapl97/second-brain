from app.bot.messages import HELP_MESSAGE


async def handle_help(update, context):
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode="Markdown"
    )

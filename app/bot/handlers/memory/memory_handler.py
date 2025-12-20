from telegram import InlineKeyboardButton, InlineKeyboardMarkup


from app.infra.notion.reminders import create_notion_reminder
from app.ai.memory_parser import MemoryParser
from app.modules.memory.repository import MemoryRepository
from app.bot.messages import (
    GENERAL_ERROR,
    GENERAL_CANCELLED,
)
from app.bot.formatters import format_memory_confirmation


async def handle_memory_text(update, context):
    """
    Recebe o texto do usuário, usa IA para interpretar
    e pede confirmação antes de salvar.
    """
    text = update.message.text

    try:
        parser = MemoryParser()
        parsed = parser.parse(text)

        # guarda a memória pendente no contexto
        context.user_data["pending_memory"] = parsed

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Salvar", callback_data="memory:confirm"),
                InlineKeyboardButton("❌ Cancelar", callback_data="memory:cancel"),
            ]
        ])

        await update.message.reply_text(
            format_memory_confirmation(parsed),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    except Exception as e:
        print(e)
        await update.message.reply_text(GENERAL_ERROR)


async def handle_memory_confirmation(update, context):
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get("pending_memory")

    if not pending:
        await query.edit_message_text(GENERAL_CANCELLED)
        return

    if query.data == "memory:confirm":
        try:
            repo = MemoryRepository()

            # 🔹 salva a memória (APENAS campos da tabela)
            memory_data = {
                "content": pending["content"],
                "memory_type": pending["memory_type"],
                "tags": pending.get("tags", []),
                "context": None,
                "source": "telegram",
            }

            saved = repo.create(memory_data)

            # 🔗 envia para Notion Calendar se for lembrete
            if pending["memory_type"] == "reminder" and pending.get("datetime"):
                create_notion_reminder(
                    title=pending["content"],
                    reminder_datetime=pending["datetime"],
                    tags=pending.get("tags", []),
                    source="telegram",
                    memory_id=saved["id"],
                )

            # limpa estado
            context.user_data.pop("pending_memory", None)

            await query.edit_message_text(
                "✅ Memória salva com sucesso!"
            )

        except Exception as e:
            print(e)
            await query.edit_message_text(GENERAL_ERROR)

    elif query.data == "memory:cancel":
        context.user_data.pop("pending_memory", None)
        await query.edit_message_text(GENERAL_CANCELLED)



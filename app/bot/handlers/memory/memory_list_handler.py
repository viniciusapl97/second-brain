from app.modules.memory.repository import MemoryRepository


async def handle_list_memories(update, context):
    """
    Telegram handler to list recent memories.
    """
    repo = MemoryRepository()
    memories = repo.list_recent(limit=5)

    if not memories:
        await update.message.reply_text("Nenhuma memória encontrada.")
        return

    text = "🧠 *Últimas memórias:*\n\n"

    for mem in memories:
        text += f"- {mem['content']}\n"

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )

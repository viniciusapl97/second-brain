from app.modules.finance.resync_service import FinanceResyncService


async def handle_resync_notion(update, context):
    await update.message.reply_text("🔄 Iniciando resync com o Notion...")

    service = FinanceResyncService()
    result = service.resync_all()

    await update.message.reply_text(
        f"""✅ Resync finalizado

📊 Total: {result['total']}
✔️ Sucesso: {result['success']}
❌ Falhas: {result['failed']}
"""
    )

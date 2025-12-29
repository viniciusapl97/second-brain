import logging
from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.ai.finance_parser import FinanceParser
from app.modules.finance.finance_service import FinanceService
from app.modules.finance.repository import FinanceRepository
from app.modules.finance.installment_service import InstallmentService
from app.modules.finance.notion_sync_service import FinanceNotionSyncService

from app.bot.messages import GENERAL_ERROR, GENERAL_CANCELLED
from app.bot.formatters import format_finance_confirmation

logger = logging.getLogger(__name__)


def _build_finance_service() -> FinanceService:
    return FinanceService(
        repository=FinanceRepository(),
        installment_service=InstallmentService(),
        notion_sync_service=FinanceNotionSyncService(),
    )


async def handle_finance_text(update, context):
    text = update.message.text

    try:
        parser = FinanceParser()
        parsed = parser.parse(text)

        context.user_data["pending_finance"] = parsed

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("✅ Salvar", callback_data="finance:confirm"),
                InlineKeyboardButton("❌ Cancelar", callback_data="finance:cancel"),
            ]
        ])

        await update.message.reply_text(
            format_finance_confirmation(parsed),
            reply_markup=keyboard,
            parse_mode="Markdown",
        )

    except Exception:
        logger.exception("Erro ao interpretar mensagem financeira")
        await update.message.reply_text(GENERAL_ERROR)


async def handle_finance_confirmation(update, context):
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get("pending_finance")

    if not pending:
        await query.edit_message_text(GENERAL_CANCELLED)
        return

    if query.data == "finance:cancel":
        context.user_data.pop("pending_finance", None)
        await query.edit_message_text(GENERAL_CANCELLED)
        return

    if query.data == "finance:confirm":
        try:
            if pending.get("needs_review"):
                await query.edit_message_text(
                    "⚠️ Não consegui entender completamente essa transação.\n"
                    "Por favor, reformule a mensagem com mais detalhes."
                )
                return

            service = _build_finance_service()

            amount = pending["amount"]
            if not amount or amount <= 0:
                raise ValueError("Valor inválido")

            tx_type = pending["transaction_type"]

            if tx_type == "expense":
                service.add_expense(
                    amount=amount,
                    description=pending["description"],
                    category=pending.get("category"),
                    due_date=date.fromisoformat(pending["transaction_date"]),
                    installments=pending.get("installments_total") or 1,
                )
            else:
                service.add_income(
                    amount=amount,
                    description=pending["description"],
                    category=pending.get("category"),
                    received_date=date.fromisoformat(pending["transaction_date"]),
                )

            context.user_data.pop("pending_finance", None)

            await query.edit_message_text(
                "💰 Transação financeira salva com sucesso."
            )

        except Exception:
            logger.exception("Erro ao salvar transação financeira")
            await query.edit_message_text(GENERAL_ERROR)

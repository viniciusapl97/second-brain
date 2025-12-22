from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import date
import logging
import uuid

from app.ai.finance_parser import FinanceParser
from app.modules.finance.repository import FinanceRepository
from app.modules.finance.installment_service import InstallmentService
from app.modules.finance.notion_sync_service import FinanceNotionSyncService

from app.bot.messages import (
    GENERAL_ERROR,
    GENERAL_CANCELLED,
)
from app.bot.formatters import format_finance_confirmation


logger = logging.getLogger(__name__)


async def handle_finance_text(update, context):
    """
    Recebe mensagem financeira, usa o FinanceParser
    e pede confirmação antes de salvar.
    """
    text = update.message.text

    try:
        parser = FinanceParser()
        parsed = parser.parse(text)

        # guarda transação pendente no contexto do usuário
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
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(GENERAL_ERROR)


async def handle_finance_confirmation(update, context):
    """
    Trata a confirmação ou cancelamento da transação financeira.
    """
    query = update.callback_query
    await query.answer()

    pending = context.user_data.get("pending_finance")

    if not pending:
        await query.edit_message_text(GENERAL_CANCELLED)
        return

    # ❌ Cancelar
    if query.data == "finance:cancel":
        context.user_data.pop("pending_finance", None)
        await query.edit_message_text(GENERAL_CANCELLED)
        return

    # ✅ Confirmar
    if query.data == "finance:confirm":
        try:
            repo = FinanceRepository()
            notion_sync = FinanceNotionSyncService()

            # 🔹 FINANCE V2: parcelamento real
            if pending.get("installments_total"):
                service = InstallmentService()

                installments = service.generate_installments(
                    transaction=pending,
                    start_due_date=date.today()
                )

                for inst in installments:
                    # 1️⃣ gera o id e salva no Supabase
                    pending["id"] = str(uuid.uuid4())

                    repo.create(pending)

                    # 2️⃣ tenta sincronizar com Notion
                    try:
                        notion_sync.sync_transaction(inst)
                    except Exception as e:
                        logger.error(
                            f"Erro ao sincronizar parcela {inst.get('id')} com Notion: {e}"
                        )

            else:
                # 🔹 transação simples (V1)
                repo.create(pending)

                try:
                    notion_sync.sync_transaction(pending)
                except Exception as e:
                    logger.error(
                        f"Erro ao sincronizar transação {pending.get('id')} com Notion: {e}"
                    )

            # limpa estado
            context.user_data.pop("pending_finance", None)

            await query.edit_message_text(
                "💰 Transação financeira salva com sucesso."
            )

        except Exception as e:
            logger.exception(e)
            await query.edit_message_text(GENERAL_ERROR)

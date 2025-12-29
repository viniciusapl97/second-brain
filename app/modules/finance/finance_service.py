from datetime import datetime, date
from typing import Optional, List

from app.modules.finance.repository import FinanceRepository
from app.modules.finance.installment_service import InstallmentService
from app.modules.finance.notion_sync_service import NotionSyncService


class FinanceService:
    def __init__(
        self,
        repository: FinanceRepository,
        installment_service: InstallmentService,
        notion_sync_service: Optional[NotionSyncService] = None,
    ):
        self.repository = repository
        self.installment_service = installment_service
        self.notion_sync_service = notion_sync_service

    # =====================
    # CREATE
    # =====================

    def add_expense(
        self,
        *,
        amount: float,
        description: str,
        category: Optional[str] = None,
        due_date: Optional[date] = None,
        installments: int = 1,
    ) -> List[dict]:
        self._validate_amount(amount)

        due_date = due_date or date.today()

        if installments > 1:
            transactions = self.installment_service.generate_installments(
                total_amount=-abs(amount),
                installments=installments,
                description=description,
                category=category,
                start_due_date=due_date,
                transaction_type="expense",
            )
        else:
            transactions = [{
                "amount": -abs(amount),
                "description": description,
                "category": category,
                "type": "expense",
                "is_installment": False,
                "due_date": due_date,
            }]

        saved = self.repository.save_many(transactions)

        self._sync_notion_safe(saved)

        return saved

    def add_income(
        self,
        *,
        amount: float,
        description: str,
        category: Optional[str] = None,
        received_date: Optional[date] = None,
    ) -> dict:
        self._validate_amount(amount)

        received_date = received_date or date.today()

        transaction = {
            "amount": abs(amount),
            "description": description,
            "category": category,
            "type": "income",
            "is_installment": False,
            "due_date": received_date,
        }

        saved = self.repository.save(transaction)

        self._sync_notion_safe([saved])

        return saved

    # =====================
    # READ
    # =====================

    def get_balance(self) -> float:
        transactions = self.repository.get_all()
        return sum(t["amount"] for t in transactions)

    def get_statement(
        self,
        *,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[dict]:
        return self.repository.get_by_period(start_date, end_date)

    # =====================
    # INTERNAL
    # =====================

    @staticmethod
    def _validate_amount(amount: float):
        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero")

    def _sync_notion_safe(self, transactions: List[dict]):
        if not self.notion_sync_service:
            return

        try:
            self.notion_sync_service.sync(transactions)
        except Exception as e:
            # Nunca quebrar o fluxo financeiro por falha externa
            print(f"[WARN] Falha ao sincronizar com Notion: {e}")

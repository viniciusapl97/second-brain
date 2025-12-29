from typing import Dict, List, Optional
from datetime import date

from app.infra.supabase.client import get_supabase_client


class FinanceRepository:
    TABLE_NAME = "transactions"

    def __init__(self):
        self.supabase = get_supabase_client()

    # =====================
    # CREATE
    # =====================

    def save(self, transaction: Dict) -> Dict:
        payload = self._to_db_payload(transaction)

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(payload)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to insert finance transaction")

        return response.data[0]

    def save_many(self, transactions: List[Dict]) -> List[Dict]:
        payloads = [self._to_db_payload(t) for t in transactions]

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(payloads)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to insert finance transactions")

        return response.data

    # =====================
    # READ
    # =====================

    def get_all(self) -> List[Dict]:
        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .order("transaction_date", desc=True)
            .execute()
        )

        return response.data or []

    def get_by_period(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Dict]:

        query = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
        )

        if start_date:
            query = query.gte("transaction_date", start_date.isoformat())

        if end_date:
            query = query.lte("transaction_date", end_date.isoformat())

        response = query.order("transaction_date", desc=False).execute()

        return response.data or []

    # =====================
    # INTERNAL
    # =====================

    def _to_db_payload(self, transaction: Dict) -> Dict:
        """
        Traduz o modelo do domínio financeiro para o modelo do banco.
        """

        return {
            "description": transaction["description"],
            "amount": transaction["amount"],
            "transaction_type": transaction["type"],
            "category": transaction.get("category"),
            "transaction_date": transaction["due_date"].isoformat(),
            "is_installment": transaction.get("is_installment", False),
            "installment_number": transaction.get("installment_number"),
            "installments_total": transaction.get("installments_total"),
        }

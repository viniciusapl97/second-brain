from typing import Dict, List, Optional
from datetime import date

from app.infra.supabase.client import get_supabase_client


class FinanceRepository:
    TABLE_NAME = "transactions"

    def __init__(self):
        self.supabase = get_supabase_client()

    def create(self, transaction: Dict) -> Dict:
        """
        Persiste uma transação financeira no Supabase.
        Espera receber um dict já validado pelo FinanceParser.
        """

        payload = {
            "description": transaction["description"],
            "amount": transaction["amount"],
            "transaction_type": transaction["transaction_type"],
            "category": transaction["category"],
            "payment_method": transaction["payment_method"],
            "account": transaction.get("account"),
            "installments_total": transaction.get("installments_total"),
            "transaction_date": transaction["transaction_date"],
        }

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .insert(payload)
            .execute()
        )

        if not response.data:
            raise RuntimeError("Failed to insert finance transaction")

        return response.data[0]

    def list_by_period(
        self,
        start_date: date,
        end_date: date
    ) -> List[Dict]:
        """
        Retorna transações dentro de um período.
        """

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .gte("transaction_date", start_date.isoformat())
            .lte("transaction_date", end_date.isoformat())
            .order("transaction_date", desc=False)
            .execute()
        )

        return response.data or []

    def list_all(self) -> List[Dict]:
        """
        Retorna todas as transações.
        """

        response = (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .order("transaction_date", desc=True)
            .execute()
        )

        return response.data or []

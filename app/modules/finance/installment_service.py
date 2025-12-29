from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Dict, List
import uuid


class InstallmentService:
    @staticmethod
    def generate_installments(
        *,
        total_amount: float,
        installments: int,
        description: str,
        category: str | None,
        start_due_date: date,
        transaction_type: str,  # "expense" | "income"
    ) -> List[Dict]:
        if installments < 2:
            raise ValueError("Parcelamento deve ter no mínimo 2 parcelas")

        amount_per_installment = round(total_amount / installments, 2)

        generated = []

        for i in range(1, installments + 1):
            due_date = start_due_date + relativedelta(months=i - 1)

            generated.append({
                "id": str(uuid.uuid4()),
                "amount": amount_per_installment,
                "description": description,
                "category": category,
                "type": transaction_type,
                "is_installment": True,
                "installment_number": i,
                "installments_total": installments,
                "due_date": due_date,
            })

        return generated

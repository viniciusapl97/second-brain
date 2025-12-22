from datetime import date
from dateutil.relativedelta import relativedelta
from typing import Dict, List
import uuid


class InstallmentService:
    @staticmethod
    def generate_installments(
        transaction: Dict,
        start_due_date: date
    ) -> List[Dict]:
        total = transaction["installments_total"]
        amount_per_installment = round(
            transaction["amount"] / total, 2
        )

        installments = []

        for i in range(1, total + 1):
            due_date = start_due_date + relativedelta(months=i - 1)

            installment = {
                **transaction,
                "id": str(uuid.uuid4()),  # 🔑 ID ÚNICO
                "amount": amount_per_installment,
                "is_installment": True,
                "installment_number": i,
                "due_date": due_date.isoformat(),
            }

            installments.append(installment)

        return installments

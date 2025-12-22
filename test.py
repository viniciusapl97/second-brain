from app.modules.finance.repository import FinanceRepository

repo = FinanceRepository()

transaction = {
    "description": "Teste FinanceRepo",
    "amount": 50.0,
    "transaction_type": "expense",
    "category": "Teste",
    "payment_method": "pix",
    "account": None,
    "installments_total": None,
    "transaction_date": "2025-12-20",
}

saved = repo.create(transaction)
print(saved)

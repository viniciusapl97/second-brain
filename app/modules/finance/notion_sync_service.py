import os
from datetime import datetime
from app.infra.notion.client import get_notion_client

# ID da database de Finanças no Notion
FINANCE_DB_ID = os.getenv("NOTION_FINANCE_DB_ID")

if not FINANCE_DB_ID:
    raise RuntimeError("NOTION_FINANCE_DB_ID não definida no ambiente")


class FinanceNotionSyncService:
    def __init__(self):
        # Usa o mesmo padrão do módulo Memory (lazy client)
        self.notion = get_notion_client()

    def sync_transaction(self, transaction: dict):
        """
        Cria uma página no Notion para a transação ou parcela.
        Mapper é defensivo para evitar KeyError.
        """
        print("🔁 Sync com Notion iniciado:", transaction.get("id"))

        self.notion.pages.create(
            parent={"database_id": FINANCE_DB_ID},
            properties=self._map_properties(transaction)
        )

        print("✅ Sync com Notion finalizado")

    def _map_properties(self, t: dict):
        """
        Mapper DEFENSIVO:
        - Nunca assume que um campo existe
        - Garante valores válidos para o Notion
        """

        # 🔑 ID (obrigatório)
        transaction_id = t.get("id")
        if not transaction_id:
            raise ValueError("Transação sem ID não pode ser sincronizada")

        # 📝 Descrição
        description = t.get("description", "Sem descrição")

        # 📅 Data (date para simples / due_date para parcelas)
        date_value = (
            t.get("date")
            or t.get("due_date")
            or datetime.utcnow().date().isoformat()
        )

        # 🔁 Tipo financeiro
        tx_type = t.get("type", "expense")

        # 💰 Valor
        amount = float(t.get("amount", 0.0))

        # 🗂️ Categoria
        category = t.get("category", "Outros")

        # 💳 Forma de pagamento
        payment_method = t.get("payment_method", "Não informado")

        # 📦 Parcelamento
        is_installment = bool(t.get("is_installment", False))

        return {
            "Transaction ID": {
                "rich_text": [
                    {"text": {"content": transaction_id}}
                ]
            },
            "Descrição": {
                "title": [
                    {"text": {"content": description}}
                ]
            },
            "Data": {
                "date": {
                    "start": (
                        date_value.isoformat()
                        if hasattr(date_value, "isoformat")
                        else date_value
                    )
                }
            },
            "Tipo": {
                "select": {"name": tx_type}
            },
            "Categoria": {
                "select": {"name": category}
            },
            "Valor": {
                "number": amount
            },
            "Conta": {
                "select": {"name": payment_method}
            },
            "Parcelado": {
                "checkbox": is_installment
            },
            "Criado em": {
                "date": {
                    "start": datetime.utcnow().isoformat()
                }
            }
        }

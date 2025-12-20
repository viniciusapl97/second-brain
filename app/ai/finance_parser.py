import json
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError

load_dotenv()


class FinanceParser:
    """
    Interpreta mensagens financeiras em português (PT-BR)
    e converte em dados estruturados para registro financeiro.
    """

    MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = f"""
Hoje é {datetime.now().strftime('%Y-%m-%d')}.

Você é um parser financeiro pessoal.

Sua única função é transformar mensagens em português
em um JSON ESTRITO seguindo exatamente este formato:

{{
  "module": "finance",
  "description": "string curta em português",
  "amount": number,
  "transaction_type": "income | expense",
  "category": "string em português",
  "payment_method": "credit | debit | pix | cash | transfer",
  "account": "string ou null",
  "installments_total": number ou null,
  "transaction_date": "YYYY-MM-DD"
}}

Regras IMPORTANTES:
- Responda APENAS com JSON válido
- Nunca explique nada
- Nunca use emojis
- amount deve ser o valor TOTAL da transação
- Se não houver parcelamento, use null em installments_total
- Se não houver conta/cartão claro, use null em account
- Se não houver data explícita, use a data de hoje
- transaction_type:
  - "expense" para gastos
  - "income" para entradas de dinheiro
- payment_method deve ser um dos valores permitidos
- category deve ser simples (ex: Alimentação, Transporte, Salário)
Exemplos importantes:
- "Recebi meu salário de R$4500" → transaction_type = "income"
- "Caiu o pagamento do freelance" → transaction_type = "income"
- "Ganhei 200 reais" → transaction_type = "income"
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)

    def parse(self, text: str) -> Dict:
        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=0.1,
            )

            raw = response.choices[0].message.content.strip()
            parsed = json.loads(raw)

            # 🔑 ORDEM CORRETA
            parsed = self._normalize(parsed)
            self._validate(parsed)

            return parsed

        except Exception as e:
            # DEBUG TEMPORÁRIO (IMPORTANTE)
            print("⚠️ FinanceParser fallback:", e)
            return self._fallback(text)

    def _fallback(self, text: str) -> Dict:
        return {
            "module": "finance",
            "description": text[:60],
            "amount": 0,
            "transaction_type": "expense",  # default conservador
            "category": "Outros",
            "payment_method": "cash",
            "account": None,
            "installments_total": None,
            "transaction_date": datetime.now().strftime("%Y-%m-%d"),
            "needs_review": True  # 👈 ADIÇÃO IMPORTANTE
        }

    def _normalize(self, data: Dict) -> Dict:
        desc = data.get("description", "").lower()

        # 🔹 normaliza transaction_type
        if data.get("transaction_type") not in {"income", "expense"}:
            if any(word in desc for word in ["recebi", "salário", "ganhei", "pagamento"]):
                data["transaction_type"] = "income"
            else:
                data["transaction_type"] = "expense"

        # 🔹 normaliza payment_method
        payment_map = {
            "credito": "credit",
            "crédito": "credit",
            "débito": "debit",
            "pix": "pix",
            "transferencia": "transfer",
            "transferência": "transfer",
            "deposito": "transfer",
            "depósito": "transfer",
            "salario": "transfer",
            "salário": "transfer",
            "bank transfer": "transfer",
        }

        pm = data.get("payment_method")
        if isinstance(pm, str):
            pm_norm = pm.lower().strip()
            data["payment_method"] = payment_map.get(pm_norm, pm_norm)

        # 🔹 regra explícita para income
        if data["transaction_type"] == "income":
            data["payment_method"] = "transfer"

        # 🔹 normaliza amount
        try:
            data["amount"] = float(data["amount"])
        except Exception:
            data["amount"] = 0

        return data




    def _validate(self, data: Dict) -> None:
        required_keys = {
            "module",
            "description",
            "amount",
            "transaction_type",
            "category",
            "payment_method",
            "account",
            "installments_total",
            "transaction_date",
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError("Missing required fields")

        if data["module"] != "finance":
            raise ValueError("Invalid module")

        if data["transaction_type"] not in {"income", "expense"}:
            raise ValueError("Invalid transaction_type")

        if data["payment_method"] not in {
            "credit", "debit", "pix", "cash", "transfer"
        }:
            raise ValueError("Invalid payment_method")

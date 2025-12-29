import json
import os
from datetime import datetime
from typing import Dict
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class FinanceParser:
    """
    Interpreta mensagens financeiras em português (PT-BR)
    e converte em dados estruturados (SEM regras de negócio).
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

            parsed = self._normalize(parsed)

            return parsed

        except Exception as e:
            print("⚠️ FinanceParser fallback:", e)
            return self._fallback(text)

    # =====================
    # INTERNAL
    # =====================

    def _fallback(self, text: str) -> Dict:
        return {
            "module": "finance",
            "description": text[:60],
            "amount": None,
            "transaction_type": "expense",
            "category": "Outros",
            "payment_method": None,
            "account": None,
            "installments_total": None,
            "transaction_date": datetime.now().strftime("%Y-%m-%d"),
            "needs_review": True,
        }

    def _normalize(self, data: Dict) -> Dict:
        data["needs_review"] = False

        # 🔹 normaliza amount
        try:
            data["amount"] = float(data.get("amount"))
        except Exception:
            data["amount"] = None
            data["needs_review"] = True

        # 🔹 normaliza transaction_type
        if data.get("transaction_type") not in {"income", "expense"}:
            data["transaction_type"] = "expense"
            data["needs_review"] = True

        # 🔹 normaliza payment_method (apenas mapeia, não valida)
        payment_map = {
            "credito": "credit",
            "crédito": "credit",
            "debito": "debit",
            "débito": "debit",
            "pix": "pix",
            "dinheiro": "cash",
            "transferencia": "transfer",
            "transferência": "transfer",
            "deposito": "transfer",
            "depósito": "transfer",
            "salario": "transfer",
            "salário": "transfer",
        }

        pm = data.get("payment_method")
        if isinstance(pm, str):
            pm_norm = pm.lower().strip()
            data["payment_method"] = payment_map.get(pm_norm, pm_norm)
        else:
            data["payment_method"] = None

        return data

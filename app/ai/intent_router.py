import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class IntentRouter:
    """
    Decide qual módulo deve processar a mensagem do usuário.
    """

    MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = """
Você é um classificador de intenção.

Classifique a mensagem do usuário em UM dos seguintes domínios:

- "memory": anotações, ideias, reflexões, lembretes, pensamentos pessoais
- "finance": gastos, compras, pagamentos, salários, entradas ou saídas de dinheiro,
             cartões, pix, débito, crédito, parcelas, faturas

Regras:
- Responda APENAS com JSON válido
- Nunca explique nada
- Nunca inclua texto fora do JSON
- Sempre use letras minúsculas

Formato obrigatório:
{
  "intent": "memory | finance",
  "confidence": number entre 0 e 1
}
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)

    def route(self, text: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0,
        )

        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)

        # validação mínima
        if parsed["intent"] not in {"memory", "finance"}:
            raise ValueError("Invalid intent returned by router")

        return parsed

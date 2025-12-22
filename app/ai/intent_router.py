from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


Intent = Literal["memory", "finance"]


class IntentRouter:
    """
    Decide qual módulo deve processar a mensagem do usuário.
    """

    MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = """
Você é um classificador de intenções.

Classifique a mensagem do usuário em UMA das opções abaixo:

- memory → anotações, ideias, reflexões, lembretes
- finance → gastos, pagamentos, salários, compras, dinheiro

Responda APENAS com uma dessas palavras:
memory
finance
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        self.client = OpenAI(api_key=api_key)

    def route(self, text: str) -> Intent:
        response = self.client.chat.completions.create(
            model=self.MODEL,
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0
        )

        intent = response.choices[0].message.content.strip().lower()

        if intent not in ("memory", "finance"):
            # fallback seguro
            return "memory"

        return intent
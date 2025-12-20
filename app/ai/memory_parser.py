import json
from typing import Dict
from datetime import datetime
from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os

load_dotenv()


class MemoryParser:
    """
    Parses free text messages (PT-BR) into structured memory data.
    """

    MODEL = "gpt-4o-mini"

    SYSTEM_PROMPT = f"""
Hoje é {datetime.now().strftime('%Y-%m-%d')}.
Você é um parser de texto. Sua única função é transformar mensagens em português
em um JSON ESTRITO seguindo exatamente este formato:

{{
  "memory_type": "note | idea | reflection | reminder",
  "content": "string em português, sem emojis",
  "tags": ["lista", "de", "tags", "em", "português"],
  "datetime": "ISO-8601 ou null"
}}

Regras IMPORTANTES:
- Responda APENAS com JSON válido
- Nunca explique nada
- Nunca traduza o conteúdo
- memory_type SEMPRE em inglês
- content e tags SEMPRE em português
- datetime DEVE ser null se não houver data
- Se houver data SEM hora, assuma 09:00
- Se não houver tags claras, gere de 1 a 3 tags simples
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")

        self.client = OpenAI(api_key=api_key)

    def parse(self, text: str) -> Dict:
        """
        Parses user input into structured memory data.
        """

        try:
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": text}
                ],
                temperature=0.1
            )

            raw_content = response.choices[0].message.content.strip()
            parsed = json.loads(raw_content)

            self._validate(parsed)
            parsed["datetime"] = self._normalize_datetime(parsed.get("datetime"))

            return parsed

        except (RateLimitError, json.JSONDecodeError, Exception):
            return self._fallback(text)

    def _normalize_datetime(self, value) -> str | None:
        """
        Normalizes datetime to ISO-8601 full format or None.
        """
        if not value:
            return None

        try:
            # já está ISO completo
            return datetime.fromisoformat(value).isoformat()
        except ValueError:
            try:
                # tenta data sem hora
                dt = datetime.strptime(value, "%Y-%m-%d")
                return dt.replace(hour=9, minute=0).isoformat()
            except ValueError:
                return None

    def _fallback(self, text: str) -> Dict:
        """
        Safe fallback when AI is unavailable.
        """
        return {
            "memory_type": "note",
            "content": text,
            "tags": [],
            "datetime": None
        }

    def _validate(self, data: Dict) -> None:
        """
        Validates AI output structure.
        """
        required_keys = {
            "memory_type",
            "content",
            "tags",
            "datetime"
        }

        if not required_keys.issubset(data.keys()):
            raise ValueError("Missing required fields in AI output")

        if data["memory_type"] not in {
            "note", "idea", "reflection", "reminder"
        }:
            raise ValueError("Invalid memory_type")

        if not isinstance(data["tags"], list):
            raise ValueError("Tags must be a list")

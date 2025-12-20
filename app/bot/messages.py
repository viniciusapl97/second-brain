"""
Bot messages.
Pattern: <MODULE>_<PURPOSE>
"""

# ---------- HELP ----------

HELP_MESSAGE = (
    "🧠 *Segundo Cérebro — Ajuda*\n\n"
    "Você pode me enviar mensagens livres como:\n\n"
    "• _Lembrete pagar cartão amanhã às 10_\n"
    "• _Ideia criar um assistente pessoal com IA_\n"
    "• _Reflexão estou rendendo melhor de manhã_\n\n"
    "📌 Comandos disponíveis:\n"
    "/help — mostra esta ajuda\n"
    "/ultimas — lista suas últimas memórias\n\n"
    "Tudo é salvo de forma organizada automaticamente."
)


# ---------- GENERAL ----------

GENERAL_START = (
    "🧠 *Segundo Cérebro ativado!*\n\n"
    "Me mande uma mensagem livre para salvar:\n"
    "• notas\n"
    "• ideias\n"
    "• reflexões\n"
    "• lembretes\n\n"
    "_Exemplo: Lembrete pagar cartão amanhã às 10_"
)

GENERAL_ERROR = (
    "❌ Ocorreu um erro ao processar sua solicitação.\n"
    "Tente novamente em alguns instantes."
)

GENERAL_CANCELLED = "❌ Operação cancelada."


# ---------- MEMORY ----------

MEMORY_CONFIRMATION = (
    "🧠 *Entendi isso como um* *{memory_type}*\n\n"
    "📌 {content}\n"
    "{datetime}"
    "🏷️ {tags}\n\n"
    "Deseja salvar?"
)

MEMORY_SAVED_GENERIC = "✅ Memória salva com sucesso!"

MEMORY_SAVED_NOTE = "📝 Nota salva!"
MEMORY_SAVED_IDEA = "💡 Ideia salva!"
MEMORY_SAVED_REFLECTION = "🧠 Reflexão salva!"
MEMORY_SAVED_REMINDER = "⏰ Lembrete salvo!"

MEMORY_NO_TAGS = "sem tags"
MEMORY_DATETIME_LINE = "⏰ {datetime}\n"
MEMORY_NO_DATETIME = ""

MEMORY_LIST_HEADER = "🕒 *Últimas memórias:*\n\n"
MEMORY_LIST_EMPTY = "📭 Nenhuma memória encontrada ainda."

MEMORY_REMINDER_SAVED = "⏰ Lembrete salvo!"

MEMORY_ADD_TO_CALENDAR_QUESTION = (
    "📅 Deseja adicionar ao calendário?"
)

MEMORY_ADD_TO_CALENDAR_CONFIRMATION = (
    "✅ Evento adicionado ao calendário!"
)

MEMORY_ADD_TO_CALENDAR_SKIPPED = (
    "👍 Tudo bem! O lembrete ficou salvo."
)

MEMORY_ADD_TO_CALENDAR_ERROR = (
    "❌ Não foi possível adicionar ao calendário."
)
from app.bot import messages

# ---------- MEMORY ----------

MEMORY_TYPE_ICON = {
    "note": "📝",
    "idea": "💡",
    "reflection": "🧠",
    "reminder": "⏰",
}


def memory_success_message(memory_type: str) -> str:
    return {
        "note": messages.MEMORY_SAVED_NOTE,
        "idea": messages.MEMORY_SAVED_IDEA,
        "reflection": messages.MEMORY_SAVED_REFLECTION,
        "reminder": messages.MEMORY_SAVED_REMINDER,
    }.get(memory_type, messages.MEMORY_SAVED_GENERIC)


def format_memory_confirmation(parsed: dict) -> str:
    datetime_line = (
        messages.MEMORY_DATETIME_LINE.format(datetime=parsed["datetime"])
        if parsed.get("datetime")
        else messages.MEMORY_NO_DATETIME
    )

    tags = (
        ", ".join(parsed["tags"])
        if parsed.get("tags")
        else messages.MEMORY_NO_TAGS
    )

    return messages.MEMORY_CONFIRMATION.format(
        memory_type=parsed["memory_type"],
        content=parsed["content"],
        datetime=datetime_line,
        tags=tags
    )

def format_memory_list(memories: list[dict]) -> str:
    if not memories:
        return messages.MEMORY_LIST_EMPTY

    lines = []

    for mem in memories:
        icon = MEMORY_TYPE_ICON.get(mem["memory_type"], "📌")
        lines.append(f"{icon} {mem['content']}")

    return messages.MEMORY_LIST_HEADER + "\n".join(lines)

def format_finance_confirmation(data: dict) -> str:
    return (
        f"*Confirme a transação financeira:*\n\n"
        f"Descrição: {data['description']}\n"
        f"Valor: R$ {data['amount']:.2f}\n"
        f"Tipo: {data['transaction_type']}\n"
        f"Categoria: {data['category']}\n"
        f"Pagamento: {data['payment_method']}\n"
        f"Data: {data['transaction_date']}"
    )

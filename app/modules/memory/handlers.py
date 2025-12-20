from app.modules.memory.service import MemoryService
from app.ai.memory_parser import MemoryParser


def handle_memory_message(raw_text: str, source: str = "telegram") -> dict:
    """
    Use case:
    - parse user text with AI
    - create memory
    - return parsed + persisted data
    """

    parser = MemoryParser()
    service = MemoryService()

    parsed = parser.parse(raw_text)

    memory = service.create(
        content=parsed["content"],
        memory_type=parsed.get("memory_type", "note"),
        tags=parsed.get("tags", []),
        context=None,
        source=source,
    )

    return {
        "data": memory,
        "parsed": parsed,
    }

from app.modules.memory.repository import MemoryRepository


class MemoryService:
    def __init__(self):
        self.repo = MemoryRepository()

    def create(
        self,
        content: str,
        memory_type: str = "note",
        tags: list[str] | None = None,
        context: str | None = None,
        source: str = "telegram",
    ) -> dict:
        data = {
            "content": content,
            "memory_type": memory_type,
            "tags": tags or [],
            "context": context,
            "source": source,
        }

        return self.repo.create(data)

    def get_by_id(self, memory_id: str) -> dict:
        memory = self.repo.get_by_id(memory_id)

        if not memory:
            raise ValueError("Memory not found")

        return memory

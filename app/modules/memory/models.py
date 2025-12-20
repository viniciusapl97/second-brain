from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

ALLOWED_MEMORY_TYPES = [
    "note",
    "idea",
    "reflection",
    "reminder"
]


@dataclass
class MemoryNote:
    content: str
    memory_type: str
    tags: List[str] = field(default_factory=list)
    context: Optional[str] = None
    source: str = "telegram"
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        return self.memory_type in ALLOWED_MEMORY_TYPES and bool(self.content)

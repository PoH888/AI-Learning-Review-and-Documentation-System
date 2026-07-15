from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Any


@dataclass(slots=True)
class LearningRecord:
    id: int
    title: str
    category: str
    duration_minutes: int
    note: str = ""
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = date.today().isoformat()
        if self.duration_minutes < 0:
            raise ValueError("duration_minutes must be non-negative")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LearningRecord":
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            category=str(data.get("category", "未分类")),
            duration_minutes=int(data.get("duration_minutes", 0)),
            note=str(data.get("note", "")),
            created_at=str(data.get("created_at", "")),
        )

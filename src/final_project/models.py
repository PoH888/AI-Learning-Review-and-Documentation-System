from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Any


@dataclass(slots=True)
class StudyReview:
    id: int
    question: str
    ai_summary: str
    understanding: str
    tags: list[str]
    created_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = date.today().isoformat()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StudyReview":
        return cls(
            id=int(data["id"]),
            question=str(data["question"]),
            ai_summary=str(data.get("ai_summary", "")),
            understanding=str(data.get("understanding", "")),
            tags=list(data.get("tags", [])),
            created_at=str(data.get("created_at", "")),
        )
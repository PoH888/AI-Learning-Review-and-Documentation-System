from __future__ import annotations

import json
from pathlib import Path

from .models import StudyReview

DEFAULT_DATA_PATH = Path("data/review.json")


class StorageError(RuntimeError):
    """Raised when stored data cannot be parsed safely."""


def load_reviews(path: Path = DEFAULT_DATA_PATH) -> list[StudyReview]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StorageError(f"数据文件不是合法 JSON：{path}") from exc
    if not isinstance(raw, list):
        raise StorageError("数据文件顶层结构必须是列表")
    return [StudyReview.from_dict(item) for item in raw]


def save_reviews(records: list[StudyReview], path: Path = DEFAULT_DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [record.to_dict() for record in records]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

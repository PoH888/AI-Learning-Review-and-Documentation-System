from __future__ import annotations

from pathlib import Path

from .analysis import count_by_category, duration_by_category, total_duration
from .models import LearningRecord
from .storage import DEFAULT_DATA_PATH, load_records, save_records
from .validators import require_non_empty, require_non_negative_int


class RecordService:
    def __init__(self, data_path: Path = DEFAULT_DATA_PATH) -> None:
        self.data_path = data_path

    def list_records(self) -> list[LearningRecord]:
        return load_records(self.data_path)

    def add_record(self, title: str, category: str, duration_minutes: int, note: str = "") -> LearningRecord:
        title = require_non_empty(title, "标题")
        category = require_non_empty(category, "分类")
        duration_minutes = require_non_negative_int(duration_minutes, "时长")
        records = self.list_records()
        next_id = max((record.id for record in records), default=0) + 1
        record = LearningRecord(
            id=next_id,
            title=title,
            category=category,
            duration_minutes=duration_minutes,
            note=note.strip(),
        )
        records.append(record)
        save_records(records, self.data_path)
        return record

    def search_records(self, keyword: str) -> list[LearningRecord]:
        keyword = require_non_empty(keyword, "关键词").lower()
        return [
            record
            for record in self.list_records()
            if keyword in record.title.lower()
            or keyword in record.category.lower()
            or keyword in record.note.lower()
        ]

    def delete_record(self, record_id: int) -> bool:
        records = self.list_records()
        kept = [record for record in records if record.id != record_id]
        if len(kept) == len(records):
            return False
        save_records(kept, self.data_path)
        return True

    def stats(self) -> dict[str, object]:
        records = self.list_records()
        return {
            "count": len(records),
            "total_duration": total_duration(records),
            "count_by_category": count_by_category(records),
            "duration_by_category": duration_by_category(records),
        }

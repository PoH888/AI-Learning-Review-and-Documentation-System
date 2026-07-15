from __future__ import annotations

from collections import Counter

from .models import LearningRecord


def total_duration(records: list[LearningRecord]) -> int:
    return sum(record.duration_minutes for record in records)


def count_by_category(records: list[LearningRecord]) -> dict[str, int]:
    return dict(Counter(record.category for record in records))


def duration_by_category(records: list[LearningRecord]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for record in records:
        totals[record.category] = totals.get(record.category, 0) + record.duration_minutes
    return totals

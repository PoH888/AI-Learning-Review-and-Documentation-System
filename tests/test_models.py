import pytest

from final_project.models import LearningRecord


def test_record_from_dict_roundtrip():
    record = LearningRecord.from_dict({"id": 1, "title": "测试", "category": "学习", "duration_minutes": 30})
    assert record.to_dict()["title"] == "测试"
    assert record.duration_minutes == 30


def test_record_rejects_negative_duration():
    with pytest.raises(ValueError):
        LearningRecord(id=1, title="bad", category="x", duration_minutes=-1)

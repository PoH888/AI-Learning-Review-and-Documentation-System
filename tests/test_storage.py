import pytest

from final_project.models import LearningRecord
from final_project.storage import StorageError, load_records, save_records


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_records(tmp_path / "missing.json") == []


def test_save_and_load_records(tmp_path):
    path = tmp_path / "records.json"
    save_records([LearningRecord(id=1, title="A", category="学习", duration_minutes=10)], path)
    records = load_records(path)
    assert len(records) == 1
    assert records[0].title == "A"


def test_bad_json_raises_storage_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{bad", encoding="utf-8")
    with pytest.raises(StorageError):
        load_records(path)

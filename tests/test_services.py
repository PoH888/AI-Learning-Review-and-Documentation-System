from final_project.services import RecordService


def test_add_search_delete_record(tmp_path):
    service = RecordService(tmp_path / "records.json")
    record = service.add_record("完成作业", "学习", 60, "JSON")
    assert record.id == 1
    assert service.search_records("json")[0].title == "完成作业"
    assert service.delete_record(1) is True
    assert service.list_records() == []


def test_stats(tmp_path):
    service = RecordService(tmp_path / "records.json")
    service.add_record("A", "学习", 10)
    service.add_record("B", "项目", 20)
    stats = service.stats()
    assert stats["count"] == 2
    assert stats["total_duration"] == 30
    assert stats["count_by_category"] == {"学习": 1, "项目": 1}

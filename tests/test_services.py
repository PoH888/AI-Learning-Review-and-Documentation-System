from final_project.services import ReviewService

def test_add_search_delete_review(tmp_path):
    service = ReviewService(tmp_path / "reviews.json")
    review = service.add_review("什么是JSON", "JS对象表示法", "理解了", ["Python", "基础"])
    assert service.search_reviews("JSON")[0].question == "什么是JSON"
    assert service.delete_review(1) is True
    assert service.list_reviews() == []

def test_update_review(tmp_path):
    service = ReviewService(tmp_path / "reviews.json")
    service.add_review("旧问题", "旧摘要", "", ["Python"])
    updated = service.update_review(1, question="新问题", tags=["Python", "进阶"])
    assert updated is not None
    assert updated.question == "新问题"
    assert updated.tags == ["Python", "进阶"]

    # 修改不存在的 id 应返回 None
    assert service.update_review(999, question="x") is None


def test_stats(tmp_path):
    service = ReviewService(tmp_path / "reviews.json")
    service.add_review("装饰器", "", "", ["Python", "进阶"])
    service.add_review("Django", "", "", ["Python", "Web"])
    stats = service.stats()
    assert stats["count"] == 2
    assert stats["count_by_tag"] == {"Python": 2, "进阶": 1, "Web": 1}

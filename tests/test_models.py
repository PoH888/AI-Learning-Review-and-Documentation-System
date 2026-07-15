from datetime import date

from final_project.models import StudyReview


def test_review_from_dict_roundtrip():
    review = StudyReview.from_dict({
        "id": 1,
        "question": "什么是装饰器",
        "ai_summary": "AOP 编程的一种实现",
        "understanding": "懂了",
        "tags": ["Python"],
    })
    assert review.to_dict()["question"] == "什么是装饰器"
    assert review.tags == ["Python"]


def test_review_auto_date():
    review = StudyReview(id=1, question="测试", ai_summary="", understanding="", tags=[])
    assert review.created_at == date.today().isoformat()
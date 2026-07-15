from __future__ import annotations

from pathlib import Path

from .analysis import count_by_date, count_by_tag, total_reviews
from .models import StudyReview
from .storage import DEFAULT_DATA_PATH, load_reviews, save_reviews
from .validators import require_non_empty


class ReviewService:
    def __init__(self, data_path: Path = DEFAULT_DATA_PATH) -> None:
        self.data_path = data_path

    def list_reviews(self) -> list[StudyReview]:
        return load_reviews(self.data_path)

    def add_review(
        self,
        question: str,
        ai_summary: str = "",
        understanding: str = "",
        tags: list[str] | None = None,
    ) -> StudyReview:
        question = require_non_empty(question, "问题")
        reviews = self.list_reviews()
        next_id = max((r.id for r in reviews), default=0) + 1
        review = StudyReview(
            id=next_id,
            question=question,
            ai_summary=ai_summary.strip(),
            understanding=understanding.strip(),
            tags=tags or [],
        )
        reviews.append(review)
        save_reviews(reviews, self.data_path)
        return review

    def search_reviews(self, keyword: str) -> list[StudyReview]:
        keyword = require_non_empty(keyword, "关键词").lower()
        return [
            review
            for review in self.list_reviews()
            if keyword in review.question.lower()
            or keyword in review.ai_summary.lower()
            or keyword in review.understanding.lower()
            or any(keyword in tag.lower() for tag in review.tags)
        ]

    def delete_review(self, review_id: int) -> bool:
        reviews = self.list_reviews()
        kept = [r for r in reviews if r.id != review_id]
        if len(kept) == len(reviews):
            return False
        save_reviews(kept, self.data_path)
        return True

    def update_review(
        self,
        review_id: int,
        *,
        question: str | None = None,
        ai_summary: str | None = None,
        understanding: str | None = None,
        tags: list[str] | None = None,
    ) -> StudyReview | None:
        reviews = self.list_reviews()
        for review in reviews:
            if review.id == review_id:
                if question is not None:
                    review.question = require_non_empty(question, "问题")
                if ai_summary is not None:
                    review.ai_summary = ai_summary.strip()
                if understanding is not None:
                    review.understanding = understanding.strip()
                if tags is not None:
                    review.tags = tags
                save_reviews(reviews, self.data_path)
                return review
        return None

    def stats(self) -> dict[str, object]:
        reviews = self.list_reviews()
        return {
            "count": total_reviews(reviews),
            "count_by_tag": count_by_tag(reviews),
            "count_by_date": count_by_date(reviews),
        }
from __future__ import annotations

from collections import Counter

from .models import StudyReview


def total_reviews(reviews: list[StudyReview]) -> int:
    return len(reviews)


def count_by_tag(reviews: list[StudyReview]) -> dict[str, int]:
    all_tags = [tag for review in reviews for tag in review.tags]
    return dict(Counter(all_tags))


def count_by_date(reviews: list[StudyReview]) -> dict[str, int]:
    return dict(Counter(review.created_at for review in reviews))

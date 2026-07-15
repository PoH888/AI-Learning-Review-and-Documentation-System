from final_project.models import StudyReview
from final_project.storage import StorageError, load_reviews, save_reviews

def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_reviews(tmp_path / "missing.json") == []

def test_save_and_load_reviews(tmp_path):
    path = tmp_path / "reviews.json"
    save_reviews([StudyReview(id=1, question="A", ai_summary="", understanding="", tags=["Python"])], path)
    reviews = load_reviews(path)
    assert reviews[0].question == "A"
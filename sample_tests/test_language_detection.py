from pathlib import Path
from file_processing.language_detection import detect_file_language

BASE = Path(__file__).parent.parent / "test_files"


def test_english_detection():
    result = detect_file_language(BASE / "sample - Copy.txt")
    top = result["fasttext_predictions"][0]["lang"]
    assert top == "en"


def test_french_detection():
    result = detect_file_language(BASE / "Sample test.pdf")
    top = result["fasttext_predictions"][0]["lang"]
    assert top == "fr"

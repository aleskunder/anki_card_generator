from src.pronunciation import fetch_pronunciation
def test_fetch_pronunciation():
    pronunciation = fetch_pronunciation("Haus", "de")
    assert "Pronunciation" in pronunciation

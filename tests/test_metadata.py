from src.metadata import add_german_metadata
def test_add_german_metadata():
    result = add_german_metadata("Haus", "noun")
    assert "noun" in result

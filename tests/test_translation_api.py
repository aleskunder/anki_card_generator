from src.translation_api import get_translations
def test_get_translations():
    translations = get_translations("test", "en", "de")
    assert len(translations) > 0

from src.card_generator import generate_anki_tsv
def test_generate_anki_tsv():
    cards = [["test", "translation", "pronunciation"]]
    generate_anki_tsv(cards, "output.tsv")
    with open("output.tsv", "r") as file:
        assert len(file.readlines()) > 0

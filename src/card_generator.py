import csv
def generate_anki_tsv(cards, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')
        for card in cards:
            writer.writerow(card)

# data/data_creation.py

import csv
import os

global vocab
vocab = {}

def load_all_vocab():
    # utiliser le dossier du module pour trouver les CSV
    folder = os.path.dirname(__file__)

    # lister tous les fichiers .csv présents dans le dossier
    try:
        CSV_FILES = [f for f in os.listdir(folder) if f.lower().endswith('.csv')]
    except Exception:
        CSV_FILES = []

    for file in CSV_FILES:
        path = os.path.join(folder, file)

        with open(path, newline="", encoding="utf-8") as f:
            # CSV uses semicolon as separator; rows look like:
            # french;english;;level, category  e.g. bon(ne);good;;basic, adjective
            reader = csv.reader(f, delimiter=';')

            for row in reader:
                if len(row) >= 2:
                    french = row[0].strip()
                    english = row[1].strip()

                    # fallback category derived from filename
                    category = os.path.splitext(file)[0].replace("en-fr_", "")
                    level = "basic"

                    # metadata column may be column 3 or 4
                    meta = None
                    if len(row) >= 4 and row[3].strip():
                        meta = row[3].strip()
                    elif len(row) >= 3 and row[2].strip():
                        meta = row[2].strip()

                    vocab[french] = [english, category]

load_all_vocab()
print()
print(vocab)
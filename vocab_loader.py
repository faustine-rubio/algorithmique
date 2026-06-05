# data/vocab_loader.py

import csv
import os
from data.vocab_data import vocab

# CSV_FILES will be discovered dynamically from the data folder at runtime

def load_all_vocab():
    # utiliser le dossier du module pour trouver les CSV
    folder = os.path.dirname(__file__)

    try:
        CSV_FILES = [f for f in os.listdir(folder) if f.lower().endswith('.csv')]
    except Exception:
        CSV_FILES = []

    for file in CSV_FILES:
        path = os.path.join(folder, file)

        with open(path, newline="", encoding="utf-8") as f:
            # CSV uses semicolon as separator and rows look like:
            # french;english;;level, category  e.g. bon(ne);good;;basic, adjective
            reader = csv.reader(f, delimiter=';')

            for row in reader:
                # need at least french and english
                if len(row) >= 2:
                    french = row[0].strip()
                    english = row[1].strip()

                    # fallback category derived from filename
                    category = os.path.splitext(file)[0].replace("en-fr_", "")
                    level = "basic"

                    # metadata may be in column 3 or 4 depending on file
                    meta = None
                    if len(row) >= 4 and row[3].strip():
                        meta = row[3].strip()
                    elif len(row) >= 3 and row[2].strip():
                        meta = row[2].strip()

                    if meta:
                        parts = [p.strip() for p in meta.split(',') if p.strip()]
                        if len(parts) >= 2:
                            # format: level, category
                            level = parts[0]
                            category = parts[1]
                        elif len(parts) == 1:
                            p = parts[0].lower()
                            if p in ("basic", "intermediate", "advanced"):
                                level = parts[0]
                            else:
                                category = parts[0]

                    vocab[french] = [english, category, level]
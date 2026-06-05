# data/data_creation.py

import csv
import os

global vocab
vocab = {}

CSV_FILES = [
    "en-fr_adjective.csv",
    "en-fr_color.csv",
    "en-fr_communication.csv",
    "en-fr_food.csv",
    "en-fr_health.csv",
    "en-fr_numbers.csv",
    "en-fr_orientation.csv",
    "en-fr_personal-information.csv",
    "en-fr_sentences.csv",
    "en-fr_shopping.csv",
    "en-fr_surrounding.csv",
    "en-fr_technology.csv",
    "en-fr_time.csv",
    "en-fr_transport.csv",
    "en-fr_verb.csv"
]

def load_all_vocab():
    folder = "data"

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
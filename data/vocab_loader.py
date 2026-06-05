# data/vocab_loader.py

import csv
import os
from vocab_data import vocab

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
    "en-fr_verb.csv",
]

def load_all_vocab():
    folder = "data"

    for file in CSV_FILES:
        path = os.path.join(folder, file)

        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) == 2:
                    english = row[0].strip()
                    french = row[1].strip()

                    vocab[english] = french
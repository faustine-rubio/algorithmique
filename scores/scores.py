import json
import os
import tkinter as tk
from tkinter import ttk

# ==========================
# Fichier de sauvegarde
# ==========================
SCORES_FILE = os.path.join(
    os.path.dirname(__file__),
    "best_scores.json"
)

DEFAULT_SCORES = {
    "quiz": 0,
    "hangman": 0,
    "memory": 0,
    "reverse": 0,
    "reading": 0
}


# ==========================
# Chargement / sauvegarde
# ==========================
def load_scores():
    if not os.path.exists(SCORES_FILE):
        save_scores(DEFAULT_SCORES)
        return DEFAULT_SCORES.copy()

    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        for key in DEFAULT_SCORES:
            data.setdefault(key, 0)

        return data

    except Exception:
        return DEFAULT_SCORES.copy()


def save_scores(scores):
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=4)


# ==========================
# Gestion des records
# ==========================
def get_best_score(game):
    scores = load_scores()
    return scores.get(game, 0)


def set_best_score(game, score):
    scores = load_scores()

    if score > scores.get(game, 0):
        scores[game] = score
        save_scores(scores)

        # Rafraîchit les labels du menu principal
        try:
            root = tk._default_root
            if root:
                root.event_generate("<<BestScoreChanged>>")
        except Exception:
            pass

        return True

    return False


# ==========================
# Fenêtre des scores
# ==========================
def open_scores():
    scores = load_scores()

    window = tk.Toplevel()
    window.title("Scores")
    window.geometry("500x350")
    window.resizable(False, False)

    title = tk.Label(
        window,
        text="🏆 Meilleurs scores",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=20)

    frame = tk.Frame(window)
    frame.pack(pady=10)

    labels = {
        "quiz": "Quiz",
        "hangman": "Pendu",
        "memory": "Memory",
        "reverse": "Traduction inversée",
        "reading": "Compréhension écrite"
    }

    for key, name in labels.items():
        row = tk.Frame(frame)
        row.pack(fill="x", pady=5)

        tk.Label(
            row,
            text=name,
            font=("Arial", 11)
        ).pack(side="left", padx=10)

        tk.Label(
            row,
            text=str(scores.get(key, 0)),
            font=("Arial", 11, "bold")
        ).pack(side="right", padx=10)

    ttk.Button(
        window,
        text="Fermer",
        command=window.destroy
    ).pack(pady=25)
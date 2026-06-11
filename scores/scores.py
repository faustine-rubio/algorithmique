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
    window.geometry("600x400")
    window.resizable(False, False)
    window.config(bg="#eef5ff")

    title = tk.Label(
    window,
    text="🏆 Best Scores",
    font=("Comic Sans MS", 24, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=20)

    frame = tk.Frame(window, bg="#eef5ff")
    frame.pack(pady=10)

    labels = {
        "quiz": "Quiz",
        "hangman": "Hangman",
        "memory": "Memory",
        "reverse": "Reverse Translation",
        "reading": "Reading Comprehension"
    }

    for key, name in labels.items():
        card = tk.Frame(
            frame,
            bg="white",
            highlightbackground="#E5E7EB",
            highlightthickness=1,
        )
        card.pack(fill="x", pady=6, padx=10)

        tk.Label(
            card,
            text=name,
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#1a3c7a",
        ).pack(side="left", padx=12, pady=8)

        tk.Label(
            card,
            text=str(scores.get(key, 0)),
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2563EB",
        ).pack(side="right", padx=12)

    close_button = tk.Button(
        window,
        text="Close",
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        relief="flat",
        cursor="hand2",
    )
    close_button.pack(pady=20)

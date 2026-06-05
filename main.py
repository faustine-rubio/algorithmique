import tkinter as tk
from tkinter import ttk

from vocab.add_word import open_add_word
from vocab.delete_word import open_delete_word
from vocab.display_vocab import open_display_vocab

from games.quiz import open_quiz
from games.hangman import open_hangman
from games.reverse_translation import open_reverse_translation
from games.reading_comprehension import open_reading_comprehension
from games.memory_game import open_memory_game

from training.training_mode import open_training_mode
from scores.scores import open_scores

from data.vocab_data import load_all_vocab
load_all_vocab()

# ==========================
# Fenêtre principale
# ==========================
root = tk.Tk()
root.title("English Vocabulary Learning")
root.geometry("900x600")
root.configure(bg="#F5F7FA")
root.resizable(False, False)

# ==========================
# Style
# ==========================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Menu.TButton",
    font=("Arial", 12, "bold"),
    padding=10
)

# ==========================
# Titre
# ==========================
title = tk.Label(
    root,
    text="English Vocabulary Learning",
    font=("Arial", 24, "bold"),
    bg="#F5F7FA",
    fg="#1F3A5F"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Learn English vocabulary through games and practice",
    font=("Arial", 12),
    bg="#F5F7FA",
    fg="#555555"
)
subtitle.pack(pady=(0, 20))

# ==========================
# Conteneur principal
# ==========================
main_frame = tk.Frame(root, bg="#F5F7FA")
main_frame.pack(expand=True)

# ==========================
# Gestion vocabulaire
# ==========================
vocab_frame = tk.LabelFrame(
    main_frame,
    text=" Vocabulary Management ",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=20,
    bg="white"
)
vocab_frame.grid(row=0, column=0, padx=20, pady=20)

ttk.Button(
    vocab_frame,
    text="Display Vocabulary",
    style="Menu.TButton",
    command=open_display_vocab
).pack(fill="x", pady=5)

ttk.Button(
    vocab_frame,
    text="Add Word",
    style="Menu.TButton",
    command=open_add_word
).pack(fill="x", pady=5)

ttk.Button(
    vocab_frame,
    text="Delete Word",
    style="Menu.TButton",
    command=open_delete_word
).pack(fill="x", pady=5)

# ==========================
# Jeux éducatifs
# ==========================
games_frame = tk.LabelFrame(
    main_frame,
    text=" Educational Games ",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=20,
    bg="white"
)
games_frame.grid(row=0, column=1, padx=20, pady=20)

ttk.Button(
    games_frame,
    text="Translation Quiz",
    style="Menu.TButton",
    command=open_quiz
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Hangman",
    style="Menu.TButton",
    command=open_hangman
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Reverse Translation",
    style="Menu.TButton",
    command=open_reverse_translation
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Reading Comprehension",
    style="Menu.TButton",
    command=open_reading_comprehension
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Memory Game",
    style="Menu.TButton",
    command=open_memory_game
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Training Mode",
    style="Menu.TButton",
    command=open_training_mode
).pack(fill="x", pady=5)

# ==========================
# Bouton quitter (bas droite)
# ==========================
bottom_quit_frame = tk.Frame(root, bg="#F5F7FA")
bottom_quit_frame.pack(fill="x", side="bottom", pady=12, padx=20)

quit_button = ttk.Button(
    bottom_quit_frame,
    text="Quitter",
    style="Menu.TButton",
    command=root.destroy
)
quit_button.pack(side="right")

# ==========================
# Lancement
# ==========================
root.mainloop()
import tkinter as tk
from tkinter import ttk
import random
import tkinter.messagebox as messagebox

from data.vocab_data import vocab


def open_training_mode():
    window = tk.Toplevel()
    window.title("Mode d'entraînement")
    window.geometry("500x300")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
        window,
        text="Mode d'entraînement",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=10)

    # Frame de contenu principal
    content_frame = tk.Frame(window)
    content_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Label pour le mot français
    french_var = tk.StringVar(value="")
    french_label = tk.Label(content_frame, textvariable=french_var, font=("Arial", 20, "bold"))
    french_label.pack(pady=(10, 5))

    # Label pour la traduction (initialement vide)
    translation_var = tk.StringVar(value="")
    translation_label = tk.Label(content_frame, textvariable=translation_var, font=("Arial", 16), fg="#333333")
    translation_label.pack(pady=(5, 15))

    # Récupère la liste des mots français
    word_list = list(vocab.keys()) if isinstance(vocab, dict) else []
    if not word_list:
        messagebox.showinfo("Info", "Aucun mot disponible pour l'entraînement.")

    current = {"word": None}

    def pick_next():
        if not word_list:
            french_var.set("")
            translation_var.set("")
            return
        current_word = random.choice(word_list)
        current["word"] = current_word
        french_var.set(f"Français : {current_word}")
        translation_var.set("")

    def show_translation():
        w = current.get("word")
        if not w:
            messagebox.showinfo("Info", "Appuyez sur 'Mot suivant' pour commencer.")
            return
        entry = vocab.get(w)
        if entry and len(entry) >= 1:
            translation_var.set(f"Anglais : {entry[0]}")
        else:
            translation_var.set("(traduction inconnue)")

    # Boutons Show / Next
    buttons_frame = tk.Frame(content_frame)
    buttons_frame.pack(pady=5)

    show_btn = ttk.Button(buttons_frame, text="Afficher traduction", command=show_translation)
    show_btn.pack(side="left", padx=8)

    next_btn = ttk.Button(buttons_frame, text="Mot suivant", command=pick_next)
    next_btn.pack(side="left", padx=8)

    # Frame pour le bouton quitter en bas à droite
    bottom_frame = tk.Frame(window, bg="#F5F7FA")
    bottom_frame.pack(fill="x", side="bottom", pady=12, padx=20)

    quit_button = ttk.Button(bottom_frame, text="Quitter", command=window.destroy)
    quit_button.pack(side="right")

    # Démarrer sur un mot
    pick_next()


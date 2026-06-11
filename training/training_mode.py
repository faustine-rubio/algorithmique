import tkinter as tk
from tkinter import ttk
import random
import tkinter.messagebox as messagebox

from data.vocab_data import vocab


def open_training_mode():
    window = tk.Toplevel()
    window.title("Mode d'entraînement")
    window.geometry("650x350")
    window.resizable(False, False)
    window.config(bg="#eef5ff")

    # Titre
    title = tk.Label(
    window,
    text="Mode d'entraînement",
    font=("Comic Sans MS", 24, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=10)

    # Frame de contenu principal
    content_frame = tk.Frame(
    window,
    bg="#eef5ff"
)
    content_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Label pour le mot français
    french_var = tk.StringVar(value="")
    french_label = tk.Label(
    content_frame,
    textvariable=french_var,
    font=("Arial", 22, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    french_label.pack(pady=(10, 5))

    # Label pour la traduction (initialement vide)
    translation_var = tk.StringVar(value="")
    translation_label = tk.Label(
    content_frame,
    textvariable=translation_var,
    font=("Arial", 18, "bold"),
    bg="#eef5ff",
    fg="#2b4c7a"
)
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

    show_btn = tk.Button(
        buttons_frame,
        text="Afficher traduction",
        command=show_translation,
        font=("Arial", 11, "bold"),
        bg="#4a90e2",
        fg="white",
        activebackground="#3b77c4",
    )
    show_btn.pack(side="left", padx=8)

    next_btn = tk.Button(
        buttons_frame,
        text="Mot suivant",
        command=pick_next,
        font=("Arial", 11, "bold"),
        bg="#66bb6a",
        fg="white",
        activebackground="#57a85a",
    )
    next_btn.pack(side="left", padx=8)

    # Frame pour le bouton quitter en bas à droite
    bottom_frame = tk.Frame(window, bg="#eef5ff")
    bottom_frame.pack(fill="x", side="bottom", pady=12, padx=20)

    quit_button = tk.Button(
        bottom_frame,
        text="Quitter",
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
    )
    quit_button.pack(side="right")

    # Démarrer sur un mot
    pick_next()


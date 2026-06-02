import tkinter as tk
from tkinter import ttk

#PORBLEMES D'IMPORTS AVEC LES AUTRES MODULES, A REVOIR !!!
from data.vocab_data import vocab

def open_display_vocab():
    window = tk.Toplevel()
    window.title("Afficher le vocabulaire")
    window.geometry("600x400")
    window.resizable(False, False)

    # ======================
    # Titre
    # ======================
    title = tk.Label(
        window,
        text="Liste du vocabulaire",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=10)

    # ======================
    # Zone texte avec scrollbar
    # ======================
    frame = tk.Frame(window)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(
        frame,
        yscrollcommand=scrollbar.set,
        font=("Arial", 12)
    )
    text_area.pack(fill="both", expand=True)

    scrollbar.config(command=text_area.yview)

    # ======================
    # Remplissage du vocabulaire
    # ======================
    if not vocab:
        text_area.insert("end", "Aucun mot disponible.\n")
    else:
        for english, french in sorted(vocab.items()):
            text_area.insert("end", f"{english}  →  {french}\n")

    text_area.config(state="disabled")

    # ======================
    # Bouton quitter (bas droite)
    # ======================
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="x")

    quit_button = ttk.Button(
        bottom_frame,
        text="Quitter",
        command=window.destroy
    )
    quit_button.pack(side="right", padx=10, pady=10)
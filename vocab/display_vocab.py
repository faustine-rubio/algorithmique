import tkinter as tk
from tkinter import ttk

from data.data_creation import vocab

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
    # Remplissage du vocabulaire (groupé par catégorie)
    # ======================
    # config tag pour titre de catégorie (gras)
    text_area.tag_configure("category", font=("Arial", 14, "bold"))

    if not vocab:
        text_area.insert("end", "Aucun mot disponible.\n")
    else:
        # construire un dict category -> list of (french, english)
        categories = {}
        for french, data in vocab.items():
            if isinstance(data, (list, tuple)) and len(data) >= 2:
                english = data[0]
                category = data[1]
            elif isinstance(data, (list, tuple)) and len(data) == 1:
                english = data[0]
                category = "unknown"
            else:
                # ancien format: valeur simple (english)
                english = data
                category = "unknown"

            categories.setdefault(category, []).append((french, english))

        for category in sorted(categories):
            # sous-titre catégorie (première lettre en majuscule, en gras)
            title = category.capitalize()
            text_area.insert("end", f"{title}\n", "category")
            for french, english in sorted(categories[category], key=lambda x: x[0]):
                text_area.insert("end", f"{french}  →  {english}\n")
            text_area.insert("end", "\n")

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
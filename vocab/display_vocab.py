import tkinter as tk
from tkinter import ttk

from data.vocab_data import vocab

BG_COLOR = "#eef5ff"
TITLE_COLOR = "#1a3c7a"
TEXT_COLOR = "#2b4c7a"

BTN_BLUE = "#4a90e2"
BTN_GREEN = "#66bb6a"
BTN_RED = "#e74c3c"

def open_display_vocab():
    window = tk.Toplevel()
    window.title("Display Vocab")
    window.geometry("700x500")
    window.config(bg="#eef5ff")
    window.resizable(False, False)

    # ======================
    # Titre
    # ======================
    title = tk.Label(
    window,
    text="Vocabulary List",
    font=("Comic Sans MS", 24, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=10)

    # ======================
    # Zone texte avec scrollbar
    # ======================
    frame = tk.Frame(
    window,
    bg="#eef5ff"
)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text_area = tk.Text(
    frame,
    yscrollcommand=scrollbar.set,
    font=("Arial", 12),
    bg="white",
    fg="#333333",
    relief="solid",
    bd=1
)
        
    text_area.pack(fill="both", expand=True)

    scrollbar.config(command=text_area.yview)

    # ======================
    # Remplissage du vocabulaire (groupé par catégorie)
    # ======================
    # config tag pour titre de catégorie (gras)
    text_area.tag_configure(
    "category",
    font=("Arial", 14, "bold"),
    foreground="#1a3c7a"
)

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
    bottom_frame = tk.Frame(window, bg="#eef5ff")
    bottom_frame.pack(fill="x")

    quit_button = tk.Button(
        bottom_frame,
        text="Exit",
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white"
    )
    quit_button.pack(side="right", padx=10, pady=10)

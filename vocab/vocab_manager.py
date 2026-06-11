import tkinter as tk
from tkinter import ttk

BG_COLOR = "#eef5ff"
TITLE_COLOR = "#1a3c7a"
TEXT_COLOR = "#2b4c7a"

BTN_BLUE = "#4a90e2"
BTN_GREEN = "#66bb6a"
BTN_RED = "#e74c3c"

def open_vocab_manager():
    window = tk.Toplevel()
    window.title("Gestionnaire de vocabulaire")
    window.geometry("600x350")
    window.resizable(False, False)
    window.config(bg="#eef5ff")

    # Titre
    title = tk.Label(
    window,
    text="Gestionnaire de vocabulaire",
    font=("Comic Sans MS", 24, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=30)

    # Espace vide pour future interface
    content_frame = tk.Frame(window, bg="#eef5ff")
    content_frame.pack(expand=True)

    # Frame pour aligner le bouton en bas à droite
    bottom_frame = tk.Frame(window, bg="#eef5ff")
    bottom_frame.pack(fill="both", expand=True)

    quit_button = tk.Button(
        bottom_frame,
        text="Quitter",
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white",
    )
    quit_button.pack(side="right", anchor="se", padx=15, pady=15)


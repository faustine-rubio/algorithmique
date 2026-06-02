import tkinter as tk
from tkinter import ttk

def open_memory_game():
    window = tk.Toplevel()
    window.title("Jeu de mémoire")
    window.geometry("500x300")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
        window,
        text="Jeu de mémoire",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=30)

    # Espace vide pour future interface
    content_frame = tk.Frame(window)
    content_frame.pack(expand=True)

    # Frame pour aligner le bouton en bas à droite
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="both", expand=True)

    quit_button = ttk.Button(
        bottom_frame,
        text="Quitter",
        command=window.destroy
    )
    quit_button.pack(side="right", anchor="se", padx=15, pady=15)


import tkinter as tk
from tkinter import ttk
import os
import csv
import tkinter.messagebox as messagebox

from data.vocab_data import vocab, delete_word_from_csv

BG_COLOR = "#eef5ff"
TITLE_COLOR = "#1a3c7a"
TEXT_COLOR = "#2b4c7a"

BTN_BLUE = "#4a90e2"
BTN_GREEN = "#66bb6a"
BTN_RED = "#e74c3c"

def open_delete_word():
    window = tk.Toplevel()
    window.title("Supprimer un mot")
    window.geometry("650x280")
    window.config(bg="#eef5ff")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
    window,
    text="Supprimer un mot",
    font=("Comic Sans MS",24,"bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=10)

    content_frame = tk.Frame(
    window,
    bg="#eef5ff"
)
    content_frame.pack(padx=20, pady=5, fill="both", expand=True)

    lbl_french = tk.Label(
    content_frame,
    text="Mot français à supprimer :",
    font=("Arial",11,"bold"),
    bg="#eef5ff",
    fg="#2b4c7a"
)
    lbl_french.grid(row=0, column=0, sticky="w", pady=6)
    entry_french = tk.Entry(
    content_frame,
    width=40,
    font=("Arial",11)
)
    entry_french.grid(row=0, column=1, pady=6)

    def on_delete():
        french = entry_french.get().strip()
        if not french:
            messagebox.showerror("Erreur", "Veuillez saisir le mot français à supprimer.")
            return

        # vérifier en mémoire
        if french not in vocab:
            messagebox.showerror("Erreur", f"Le mot '{french}' n'existe pas dans le vocabulaire.")
            return

        # confirmation
        confirm = messagebox.askyesno("Confirmer la suppression", f"Êtes-vous sûr de vouloir supprimer '{french}' ?")
        if not confirm:
            return

        # déterminer la catégorie si disponible
        data = vocab.get(french)
        category = None
        if isinstance(data, (list, tuple)) and len(data) >= 2:
            category = data[1]

        # dossier data (projetroot/data)
        data_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        if not os.path.isdir(data_folder):
            data_folder = os.path.dirname(__file__)

        # utiliser le helper centralisé pour supprimer
        removed = delete_word_from_csv(french, category)
        if removed:
            messagebox.showinfo("Succès", f"Le mot '{french}' a été supprimé.")
            entry_french.delete(0, 'end')
        else:
            messagebox.showerror("Erreur", f"Impossible de trouver et supprimer '{french}' dans les fichiers CSV.")

    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="x", pady=8)

    quit_button = tk.Button(
    bottom_frame,
    text="Quitter",
    command=window.destroy,
    font=("Arial",11,"bold"),
    bg="#7f8c8d",
    fg="white"
)
    quit_button.pack(side="right", padx=10, pady=5)

    delete_button = tk.Button(
    bottom_frame,
    text="Supprimer",
    command=on_delete,
    font=("Arial",11,"bold"),
    bg="#e74c3c",
    fg="white"
)
    delete_button.pack(side="right", padx=10, pady=5)

import tkinter as tk
from tkinter import ttk
import os
import tkinter.messagebox as messagebox

from data.vocab_data import vocab, save_word_to_csv

BG_COLOR = "#eef5ff"
TITLE_COLOR = "#1a3c7a"
TEXT_COLOR = "#2b4c7a"

BTN_BLUE = "#4a90e2"
BTN_GREEN = "#66bb6a"
BTN_RED = "#e74c3c"

def open_add_word():
    window = tk.Toplevel()
    window.title("Add Word")
    window.geometry("650x350")
    window.config(bg="#eef5ff")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
    window,
    text="Add Word",
    font=("Comic Sans MS", 24, "bold"),
    bg="#eef5ff",
    fg="#1a3c7a"
)
    title.pack(pady=10)

    # Frame de contenu pour le formulaire
    content_frame = tk.Frame(
    window,
    bg="#eef5ff"
)
    content_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Labels et champs
    lbl_french = tk.Label(content_frame, text="French word:",font=("Arial", 11, "bold"),
bg="#eef5ff",
fg="#2b4c7a")
    lbl_french.grid(row=0, column=0, sticky="w", pady=4)
    entry_french = tk.Entry(
    content_frame,
    width=40,
    font=("Arial",11)
)
    entry_french.grid(row=0, column=1, pady=4)

    lbl_english = tk.Label(content_frame, text="English word:",font=("Arial", 11, "bold"),
bg="#eef5ff",
fg="#2b4c7a")
    lbl_english.grid(row=1, column=0, sticky="w", pady=4)
    entry_english = tk.Entry(
    content_frame,
    width=40,
    font=("Arial",11)
)
    entry_english.grid(row=1, column=1, pady=4)

    lbl_category = tk.Label(content_frame, text="Category:",font=("Arial", 11, "bold"),
bg="#eef5ff",
fg="#2b4c7a")
    lbl_category.grid(row=2, column=0, sticky="w", pady=4)
    entry_category = tk.Entry(
    content_frame,
    width=40,
    font=("Arial",11)
)
    entry_category.grid(row=2, column=1, pady=4)

    def on_validate():
        french = entry_french.get().strip()
        english = entry_english.get().strip()
        category = entry_category.get().strip()
        # Forcer le niveau à "basic"
        level = "basic"

        if not french or not english:
            messagebox.showerror("Error", "Please enter the French word and its English equivalent.")
            return

        if not category:
            category = "unknown"

        # Met à jour le dictionnaire global `vocab`
        vocab[french] = [english, category, level]

        # Persister via helper centralisé
        try:
            save_word_to_csv(french, english, category, level)
            messagebox.showinfo("Success", f"The word '{french}' has been added and saved.")

            # effacer les champs
            entry_french.delete(0, "end")
            entry_english.delete(0, "end")
            entry_category.delete(0, "end")
            
        except Exception as e:
            messagebox.showerror("Error", f"Unable to save the word: {e}")
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="x", pady=10)

    quit_button = tk.Button(
    bottom_frame,
    text="Exit",
    command=window.destroy,
    font=("Arial",11,"bold"),
    bg="#e74c3c",
    fg="white"
)
    quit_button.pack(side="right", padx=10, pady=5)

    validate_button = tk.Button(
    bottom_frame,
    text="Validate",
    command=on_validate,
    font=("Arial",11,"bold"),
    bg="#4a90e2",
    fg="white"
)
    validate_button.pack(side="right", padx=10, pady=5)

import tkinter as tk
from tkinter import ttk
import os
import tkinter.messagebox as messagebox

from data.vocab_data import vocab, save_word_to_csv


def open_add_word():
    window = tk.Toplevel()
    window.title("Ajouter un mot")
    window.geometry("500x300")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
        window,
        text="Ajouter un mot",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=10)

    # Frame de contenu pour le formulaire
    content_frame = tk.Frame(window)
    content_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Labels et champs
    lbl_french = tk.Label(content_frame, text="Mot français:")
    lbl_french.grid(row=0, column=0, sticky="w", pady=4)
    entry_french = tk.Entry(content_frame, width=40)
    entry_french.grid(row=0, column=1, pady=4)

    lbl_english = tk.Label(content_frame, text="Mot anglais:")
    lbl_english.grid(row=1, column=0, sticky="w", pady=4)
    entry_english = tk.Entry(content_frame, width=40)
    entry_english.grid(row=1, column=1, pady=4)

    lbl_category = tk.Label(content_frame, text="Catégorie:")
    lbl_category.grid(row=2, column=0, sticky="w", pady=4)
    entry_category = tk.Entry(content_frame, width=40)
    entry_category.grid(row=2, column=1, pady=4)

    lbl_level = tk.Label(content_frame, text="Niveau (optionnel):")
    lbl_level.grid(row=3, column=0, sticky="w", pady=4)
    entry_level = tk.Entry(content_frame, width=40)
    entry_level.insert(0, "basic")
    entry_level.grid(row=3, column=1, pady=4)

    def on_validate():
        french = entry_french.get().strip()
        english = entry_english.get().strip()
        category = entry_category.get().strip()
        level = entry_level.get().strip() or "basic"

        if not french or not english:
            messagebox.showerror("Erreur", "Veuillez renseigner le mot français et le mot anglais.")
            return

        if not category:
            # fallback: essayer dériver depuis le nom du fichier si possible
            category = "unknown"

        # Met à jour le dictionnaire global `vocab`
        vocab[french] = [english, category, level]

        # Persister dans le CSV correspondant
        try:
            # normaliser le nom de catégorie pour le nom de fichier
            cat_slug = category.lower().strip().replace(' ', '-') if category else 'custom'
            if cat_slug in ('unknown', ''):
                cat_slug = 'custom'

            csv_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            # si le dossier data n'existe pas (rare), tombera sur le dossier relatif 'data'
            if not os.path.isdir(csv_folder):
                csv_folder = 'data'

            csv_path = os.path.join(csv_folder, f"en-fr_{cat_slug}.csv")


            # Persister via helper centralisé
            save_word_to_csv(french, english, category, level)
            messagebox.showinfo("Succès", f"Le mot '{french}' a été ajouté et enregistré.")

            # effacer les champs
            entry_french.delete(0, "end")
            entry_english.delete(0, "end")
            entry_category.delete(0, "end")
            entry_level.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'enregistrer le mot: {e}")

    # Frame pour aligner les boutons en bas
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="x", pady=10)

    quit_button = ttk.Button(bottom_frame, text="Quitter", command=window.destroy)
    quit_button.pack(side="right", padx=10, pady=5)

    validate_button = ttk.Button(bottom_frame, text="Valider", command=on_validate)
    validate_button.pack(side="right", padx=10, pady=5)

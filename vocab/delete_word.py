import tkinter as tk
from tkinter import ttk
import os
import csv
import tkinter.messagebox as messagebox

from data.data_creation import vocab


def open_delete_word():
    window = tk.Toplevel()
    window.title("Supprimer un mot")
    window.geometry("500x200")
    window.resizable(False, False)

    # Titre
    title = tk.Label(
        window,
        text="Supprimer un mot",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=10)

    content_frame = tk.Frame(window)
    content_frame.pack(padx=20, pady=5, fill="both", expand=True)

    lbl_french = tk.Label(content_frame, text="Mot français à supprimer:")
    lbl_french.grid(row=0, column=0, sticky="w", pady=6)
    entry_french = tk.Entry(content_frame, width=40)
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

        # si catégorie connue, cibler le fichier, sinon parcourir tous les CSV
        targets = []
        if category:
            slug = category.lower().strip().replace(' ', '-')
            targets = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.lower().endswith('.csv') and f"en-fr_{slug}" in f.lower()]

        if not targets:
            # fallback: tous les csv
            targets = [os.path.join(data_folder, f) for f in os.listdir(data_folder) if f.lower().endswith('.csv')]

        removed = False
        for path in targets:
            try:
                rows = []
                changed = False
                with open(path, newline='', encoding='utf-8') as rf:
                    reader = csv.reader(rf, delimiter=';')
                    for row in reader:
                        if not row:
                            continue
                        first = row[0].strip() if len(row) > 0 else ''
                        if first == french:
                            changed = True
                            removed = True
                            continue
                        rows.append(row)

                if changed:
                    # réécrire le fichier sans les lignes supprimées
                    with open(path, 'w', newline='', encoding='utf-8') as wf:
                        writer = csv.writer(wf, delimiter=';')
                        for r in rows:
                            writer.writerow(r)
            except Exception:
                # ignorer les erreurs de fichier individuel
                continue

        if removed:
            # supprimer de la mémoire
            try:
                del vocab[french]
            except KeyError:
                pass
            messagebox.showinfo("Succès", f"Le mot '{french}' a été supprimé.")
            entry_french.delete(0, 'end')
        else:
            messagebox.showerror("Erreur", f"Impossible de trouver et supprimer '{french}' dans les fichiers CSV.")

    bottom_frame = tk.Frame(window)
    bottom_frame.pack(fill="x", pady=8)

    delete_button = ttk.Button(bottom_frame, text="Supprimer", command=on_delete)
    delete_button.pack(side="right", padx=10)

    quit_button = ttk.Button(bottom_frame, text="Quitter", command=window.destroy)
    quit_button.pack(side="right")

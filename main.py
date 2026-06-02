import tkinter as tk
from tkinter import ttk

# ==========================
# Fenêtre principale
# ==========================
root = tk.Tk()
root.title("English Vocabulary Learning")
root.geometry("900x600")
root.configure(bg="#F5F7FA")
root.resizable(False, False)

# ==========================
# Style
# ==========================
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Menu.TButton",
    font=("Arial", 12, "bold"),
    padding=10
)

# ==========================
# Titre
# ==========================
title = tk.Label(
    root,
    text="English Vocabulary Learning",
    font=("Arial", 24, "bold"),
    bg="#F5F7FA",
    fg="#1F3A5F"
)
title.pack(pady=(20, 5))

subtitle = tk.Label(
    root,
    text="Learn English vocabulary through games and practice",
    font=("Arial", 12),
    bg="#F5F7FA",
    fg="#555555"
)
subtitle.pack(pady=(0, 20))

# ==========================
# Conteneur principal
# ==========================
main_frame = tk.Frame(root, bg="#F5F7FA")
main_frame.pack(expand=True)

# ==========================
# Gestion vocabulaire
# ==========================
vocab_frame = tk.LabelFrame(
    main_frame,
    text=" Vocabulary Management ",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=20,
    bg="white"
)
vocab_frame.grid(row=0, column=0, padx=20, pady=20)

ttk.Button(
    vocab_frame,
    text="Display Vocabulary",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    vocab_frame,
    text="Add Word",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    vocab_frame,
    text="Modify Word",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    vocab_frame,
    text="Delete Word",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

# ==========================
# Jeux
# ==========================
games_frame = tk.LabelFrame(
    main_frame,
    text=" Educational Games ",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=20,
    bg="white"
)
games_frame.grid(row=0, column=1, padx=20, pady=20)

ttk.Button(
    games_frame,
    text="Translation Quiz",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Hangman",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Reverse Translation",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Reading Comprehension",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

ttk.Button(
    games_frame,
    text="Memory Game",
    style="Menu.TButton",
    command=lambda: None
).pack(fill="x", pady=5)

# ==========================
# Progression
# ==========================
progress_frame = tk.LabelFrame(
    root,
    text=" Progress ",
    font=("Arial", 12, "bold"),
    padx=20,
    pady=10,
    bg="white"
)
progress_frame.pack(fill="x", padx=40, pady=10)

progress_label = tk.Label(
    progress_frame,
    text="No score available yet",
    font=("Arial", 11),
    bg="white"
)
progress_label.pack()

# ==========================
# Bouton quitter
# ==========================
quit_button = ttk.Button(
    root,
    text="Quit",
    style="Menu.TButton",
    command=root.destroy
)
quit_button.pack(pady=20)

# ==========================
# Lancement
# ==========================
root.mainloop()
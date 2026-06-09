import os
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

from vocab.add_word import open_add_word
from vocab.delete_word import open_delete_word
from vocab.display_vocab import open_display_vocab

from games.quiz import open_quiz
from games.hangman import open_hangman
from games.reverse_translation import open_reverse_translation
from games.reading_comprehension import open_reading_comprehension
from games.memory_game import open_memory_game

from training.training_mode import open_training_mode
from scores.scores import open_scores

from data.vocab_data import load_all_vocab
load_all_vocab()

root = tk.Tk()

# ==========================
# Couleurs & constantes
# ==========================
BG_COLOR       = "#FAF8F4"
WHITE          = "#FFFFFF"
NAVY           = "#1A2E5A"
BLUE_BTN       = "#2563EB"
BLUE_BTN_HOV   = "#1D4ED8"
GRAY_TEXT      = "#6B7280"
BORDER_COLOR   = "#E5E7EB"
CARD_RADIUS    = 16   # simulé via surligneur Canvas

CARD_ICONS = {
    "Vocabulaire":  "📖",
    "Jeux":         "🎮",
    "Entraînement": "🏋",
    "Progrès":      "📈",
    "Paramètres":   "⚙️",
}

# ==========================
# BACKGROUND IMAGE
# ==========================
image_path = os.path.join(os.path.dirname(__file__), "image_fond.png")

bg_photo = None
bg_label = tk.Label(root, bg=BG_COLOR)
if os.path.exists(image_path):
    if Image is not None and ImageTk is not None:
        img = Image.open(image_path)
        img = img.resize((960, 620))  # taille initiale
        bg_photo = ImageTk.PhotoImage(img)
    else:
        try:
            bg_photo = tk.PhotoImage(file=image_path)
        except tk.TclError:
            bg_photo = None
    if bg_photo is not None:
        bg_label.configure(image=bg_photo)
        bg_label.image = bg_photo

bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ==========================
# Fenêtre principale
# ==========================
root.title("Vocable – Apprentissage de vocabulaire anglais")
root.geometry("960x620")
root.minsize(860, 580)
root.maxsize(1280, 900)
root.resizable(True, True)
root.configure(bg=BG_COLOR)

# ==========================
# Helpers style
# ==========================
def make_rounded_button(parent, text, command, bg=BLUE_BTN, fg=WHITE,
                         font=("Helvetica", 10, "bold"), padx=0, pady=6, width=14):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        font=font,
        relief="flat",
        cursor="hand2",
        activebackground=BLUE_BTN_HOV,
        activeforeground=WHITE,
        bd=0,
        padx=padx,
        pady=pady,
        width=width,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=BLUE_BTN_HOV))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# ==========================
# En-tête (logo + stats)
# ==========================
header = tk.Frame(root, bg=BG_COLOR)
header.pack(fill="x", padx=30, pady=(20, 0))

# ---- Bienvenue (gauche) ----
welcome_frame = tk.Frame(header, bg=WHITE, relief="flat", bd=0,
                          highlightbackground=BORDER_COLOR, highlightthickness=1)
welcome_frame.pack(side="left")

tk.Label(welcome_frame, text="👤", font=("Helvetica", 20), bg=WHITE)\
    .grid(row=0, column=0, rowspan=2, padx=(12, 8), pady=10)
tk.Label(welcome_frame, text="Bienvenue !", font=("Helvetica", 11, "bold"),
         bg=WHITE, fg=NAVY).grid(row=0, column=1, sticky="w", padx=(0, 14))
tk.Label(welcome_frame, text="Apprends, joue\net progresse en anglais !",
         font=("Helvetica", 9), bg=WHITE, fg=GRAY_TEXT, justify="left")\
    .grid(row=1, column=1, sticky="w", padx=(0, 14))

# ---- Logo central ----
center_frame = tk.Frame(header, bg=BG_COLOR)
center_frame.pack(side="left", expand=True)

tk.Label(center_frame, text="VOCABLE", font=("Helvetica", 32, "bold"),
         bg=BG_COLOR, fg=NAVY).pack()
tk.Label(center_frame, text="Language Learning Center",
         font=("Helvetica", 11), bg=BG_COLOR, fg=GRAY_TEXT).pack()

# ---- Stats (droite) ----
stats_frame = tk.Frame(header, bg=WHITE, relief="flat", bd=0,
                        highlightbackground=BORDER_COLOR, highlightthickness=1)
stats_frame.pack(side="right")

tk.Label(stats_frame, text="🏆  Meilleur score", font=("Helvetica", 9),
         bg=WHITE, fg=GRAY_TEXT).grid(row=0, column=0, sticky="w", padx=14, pady=(8, 0))
tk.Label(stats_frame, text="1250", font=("Helvetica", 18, "bold"),
         bg=WHITE, fg=NAVY).grid(row=1, column=0, sticky="w", padx=14)
tk.Label(stats_frame, text="📊  Mots appris", font=("Helvetica", 9),
         bg=WHITE, fg=GRAY_TEXT).grid(row=2, column=0, sticky="w", padx=14, pady=(6, 0))
tk.Label(stats_frame, text="85", font=("Helvetica", 18, "bold"),
         bg=WHITE, fg=NAVY).grid(row=3, column=0, sticky="w", padx=14, pady=(0, 8))

# ==========================
# Cartes principales
# ==========================
cards_area = tk.Frame(root, bg=BG_COLOR)
cards_area.pack(expand=True, fill="both", padx=20, pady=20)

# Centrage des 5 cartes
for i in range(5):
    cards_area.columnconfigure(i, weight=1)
cards_area.rowconfigure(0, weight=1)


def make_card(parent, col, icon, title, subtitle, btn_text, command):
    card = tk.Frame(parent, bg=WHITE, relief="flat", bd=0,
                    highlightbackground=BORDER_COLOR, highlightthickness=1)
    card.grid(row=0, column=col, padx=8, pady=4, sticky="nsew")

    # Icône
    icon_bg_colors = ["#D1FAE5", "#FEF3C7", "#DBEAFE", "#EDE9FE", "#FCE7F3"]
    ic_bg = icon_bg_colors[col % len(icon_bg_colors)]
    icon_circle = tk.Label(card, text=icon, font=("Helvetica", 24),
                           bg=ic_bg, width=3, height=1, relief="flat")
    icon_circle.pack(pady=(24, 10))

    tk.Label(card, text=title, font=("Helvetica", 12, "bold"),
             bg=WHITE, fg=NAVY).pack()
    tk.Label(card, text=subtitle, font=("Helvetica", 9), bg=WHITE,
             fg=GRAY_TEXT, wraplength=140, justify="center").pack(pady=(4, 14))

    btn = make_rounded_button(card, btn_text, command)
    btn.pack(pady=(0, 20))
    return card


# ---- Vocabulaire ----
def open_vocab_menu():
    win = tk.Toplevel(root)
    win.title("Vocabulaire")
    win.geometry("300x200")
    win.configure(bg=BG_COLOR)
    tk.Label(win, text="Vocabulaire", font=("Helvetica", 14, "bold"),
             bg=BG_COLOR, fg=NAVY).pack(pady=14)
    make_rounded_button(win, "Afficher", open_display_vocab, width=18).pack(pady=4)
    make_rounded_button(win, "Ajouter un mot", open_add_word, width=18).pack(pady=4)
    make_rounded_button(win, "Supprimer un mot", open_delete_word, width=18).pack(pady=4)

make_card(cards_area, 0, "📖", "VOCABULAIRE",
          "Gérer et consulter\nla liste des mots",
          "Accéder", open_vocab_menu)

# ---- Jeux ----
def open_games_menu():
    win = tk.Toplevel(root)
    win.title("Jeux")
    win.geometry("300x280")
    win.configure(bg=BG_COLOR)
    tk.Label(win, text="Jeux éducatifs", font=("Helvetica", 14, "bold"),
             bg=BG_COLOR, fg=NAVY).pack(pady=14)
    make_rounded_button(win, "Quiz de traduction", open_quiz, width=22).pack(pady=3)
    make_rounded_button(win, "Pendu", open_hangman, width=22).pack(pady=3)
    make_rounded_button(win, "Traduction inversée", open_reverse_translation, width=22).pack(pady=3)
    make_rounded_button(win, "Compréhension écrite", open_reading_comprehension, width=22).pack(pady=3)
    make_rounded_button(win, "Jeu de mémoire", open_memory_game, width=22).pack(pady=3)

make_card(cards_area, 1, "🎮", "JEUX",
          "Joue et révise ton\nvocabulaire",
          "Jouer", open_games_menu)

# ---- Entraînement ----
make_card(cards_area, 2, "🏋", "ENTRAÎNEMENT",
          "Révise les mots\nsans pression",
          "S'entraîner", open_training_mode)

# ---- Progrès ----
make_card(cards_area, 3, "📈", "PROGRÈS",
          "Voir tes scores\net statistiques",
          "Voir", open_scores)

# ---- Paramètres (placeholder) ----
def open_settings():
    win = tk.Toplevel(root)
    win.title("Paramètres")
    win.geometry("300x160")
    win.configure(bg=BG_COLOR)
    tk.Label(win, text="Paramètres", font=("Helvetica", 14, "bold"),
             bg=BG_COLOR, fg=NAVY).pack(pady=20)
    tk.Label(win, text="Options et préférences\n(à implémenter)",
             font=("Helvetica", 10), bg=BG_COLOR, fg=GRAY_TEXT).pack()

make_card(cards_area, 4, "⚙️", "PARAMÈTRES",
          "Options et\npréférences",
          "Ouvrir", open_settings)

# ==========================
# Pied de page
# ==========================
footer = tk.Frame(root, bg=BG_COLOR)
footer.pack(fill="x", padx=30, pady=(0, 14))

quote_frame = tk.Frame(footer, bg=WHITE, relief="flat", bd=0,
                        highlightbackground=BORDER_COLOR, highlightthickness=1)
quote_frame.pack(side="left", expand=True, fill="x", padx=(0, 10), pady=2)
tk.Label(quote_frame,
         text='" Every day is a chance to learn something new. "',
         font=("Helvetica", 10, "italic"), bg=WHITE, fg=NAVY).pack(pady=4)
tk.Label(quote_frame, text="– Learn • Play • Grow",
         font=("Helvetica", 9), bg=WHITE, fg=GRAY_TEXT).pack(pady=(0, 6))

# Bouton À propos
about_btn = make_rounded_button(
    footer, "ℹ  À propos",
    lambda: messagebox.showinfo("À propos", "Vocable – English Vocabulary Learning\nv1.0"),
    bg=WHITE, fg=NAVY, width=12
)
about_btn.config(highlightbackground=BORDER_COLOR, highlightthickness=1)
about_btn.pack(side="left", pady=2)

# Bouton Quitter
quit_btn = make_rounded_button(footer, "⇥  Quitter", root.destroy,
                                bg=WHITE, fg=NAVY, width=12)
quit_btn.config(highlightbackground=BORDER_COLOR, highlightthickness=1)
quit_btn.pack(side="right", pady=2)

# ==========================
# Lancement
# ==========================
root.mainloop()
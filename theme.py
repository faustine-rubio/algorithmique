"""
theme.py – Centralized dark theme for English Vocabulary Learning
Apply with: apply_theme(window)
"""
import tkinter as tk
from tkinter import ttk

# ─── Palette ────────────────────────────────────────────────────────────────
BG          = "#0F1117"   # background principal (deep navy-black)
BG_CARD     = "#1A1D27"   # cartes / labelframes
BG_INPUT    = "#252836"   # champs de saisie
BG_HOVER    = "#2E3347"   # hover état

FG_PRIMARY  = "#E8EAF0"   # texte principal
FG_SECONDARY= "#8B92A8"   # texte secondaire / labels
FG_MUTED    = "#555D75"   # texte désactivé

ACCENT      = "#6C8EFF"   # bleu-violet (bouton principal)
ACCENT_DARK = "#4F6FE0"   # hover accent
SUCCESS     = "#4ECBA0"   # vert succès
WARNING     = "#F5A623"   # orange avertissement
DANGER      = "#E05C6B"   # rouge danger
PURPLE      = "#A78BFA"   # violet (catégories)

BORDER      = "#2A2E40"   # bordures subtiles
RADIUS      = 8           # arrondi général (utilisé dans Canvas)

# ─── Fonts ──────────────────────────────────────────────────────────────────
FONT_TITLE   = ("Segoe UI", 22, "bold")
FONT_HEADING = ("Segoe UI", 14, "bold")
FONT_BODY    = ("Segoe UI", 11)
FONT_SMALL   = ("Segoe UI", 9)
FONT_MONO    = ("Consolas", 11)
FONT_DISPLAY = ("Segoe UI", 28, "bold")
FONT_BTN     = ("Segoe UI", 10, "bold")

# ─── TTK Style ───────────────────────────────────────────────────────────────
def apply_ttk_style():
    style = ttk.Style()
    style.theme_use("clam")

    # ── Frame / LabelFrame ──────────────────────────────────────────────────
    style.configure("TFrame",       background=BG)
    style.configure("Card.TFrame",  background=BG_CARD)

    style.configure(
        "TLabelframe",
        background=BG_CARD,
        foreground=FG_SECONDARY,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        relief="flat",
    )
    style.configure(
        "TLabelframe.Label",
        background=BG_CARD,
        foreground=ACCENT,
        font=FONT_HEADING,
    )

    # ── Buttons ─────────────────────────────────────────────────────────────
    # Primary (accent bleu)
    style.configure(
        "Primary.TButton",
        background=ACCENT,
        foreground="#FFFFFF",
        font=FONT_BTN,
        padding=(14, 8),
        borderwidth=0,
        relief="flat",
        focusthickness=0,
    )
    style.map(
        "Primary.TButton",
        background=[("active", ACCENT_DARK), ("pressed", ACCENT_DARK)],
        foreground=[("active", "#FFFFFF")],
    )

    # Secondary (outline subtile)
    style.configure(
        "Secondary.TButton",
        background=BG_INPUT,
        foreground=FG_PRIMARY,
        font=FONT_BTN,
        padding=(14, 8),
        borderwidth=1,
        relief="flat",
        focusthickness=0,
    )
    style.map(
        "Secondary.TButton",
        background=[("active", BG_HOVER), ("pressed", BG_HOVER)],
        foreground=[("active", FG_PRIMARY)],
    )

    # Danger
    style.configure(
        "Danger.TButton",
        background=DANGER,
        foreground="#FFFFFF",
        font=FONT_BTN,
        padding=(14, 8),
        borderwidth=0,
        relief="flat",
        focusthickness=0,
    )
    style.map(
        "Danger.TButton",
        background=[("active", "#C0485A"), ("pressed", "#C0485A")],
    )

    # Success
    style.configure(
        "Success.TButton",
        background=SUCCESS,
        foreground="#0F1117",
        font=FONT_BTN,
        padding=(14, 8),
        borderwidth=0,
        relief="flat",
        focusthickness=0,
    )
    style.map(
        "Success.TButton",
        background=[("active", "#38A882"), ("pressed", "#38A882")],
    )

    # Alias générique pour la compatibilité avec l'ancien "Menu.TButton"
    style.configure(
        "Menu.TButton",
        background=BG_INPUT,
        foreground=FG_PRIMARY,
        font=FONT_BTN,
        padding=(14, 9),
        borderwidth=0,
        relief="flat",
        focusthickness=0,
    )
    style.map(
        "Menu.TButton",
        background=[("active", ACCENT), ("pressed", ACCENT_DARK)],
        foreground=[("active", "#FFFFFF")],
    )

    # ── Entry ────────────────────────────────────────────────────────────────
    style.configure(
        "TEntry",
        fieldbackground=BG_INPUT,
        foreground=FG_PRIMARY,
        insertcolor=FG_PRIMARY,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        padding=(8, 6),
        relief="flat",
    )
    style.map(
        "TEntry",
        fieldbackground=[("focus", BG_HOVER)],
        bordercolor=[("focus", ACCENT)],
    )

    # ── Scrollbar ────────────────────────────────────────────────────────────
    style.configure(
        "Vertical.TScrollbar",
        background=BG_INPUT,
        troughcolor=BG,
        bordercolor=BG,
        arrowcolor=FG_SECONDARY,
        relief="flat",
    )
    style.map(
        "Vertical.TScrollbar",
        background=[("active", BG_HOVER)],
    )

    # ── Combobox ────────────────────────────────────────────────────────────
    style.configure(
        "TCombobox",
        fieldbackground=BG_INPUT,
        background=BG_INPUT,
        foreground=FG_PRIMARY,
        selectbackground=ACCENT,
        selectforeground="#FFFFFF",
        bordercolor=BORDER,
        arrowcolor=FG_SECONDARY,
        padding=(8, 6),
        relief="flat",
    )


# ─── Appliquer le fond sombre à une fenêtre tk ──────────────────────────────
def apply_theme(window):
    """Applique le thème sombre à une fenêtre Toplevel ou Tk."""
    apply_ttk_style()
    window.configure(bg=BG)


# ─── Helpers de widgets pré-stylisés ────────────────────────────────────────
def make_title(parent, text, size=22):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", size, "bold"),
        bg=BG,
        fg=FG_PRIMARY,
    )


def make_subtitle(parent, text):
    return tk.Label(
        parent,
        text=text,
        font=FONT_BODY,
        bg=BG,
        fg=FG_SECONDARY,
    )


def make_card(parent, **kwargs):
    """LabelFrame stylisé comme une carte."""
    return tk.Frame(parent, bg=BG_CARD, bd=0, highlightthickness=1,
                    highlightbackground=BORDER, **kwargs)


def make_label(parent, text, secondary=False, mono=False, size=None):
    font = FONT_MONO if mono else (FONT_BODY if not size else ("Segoe UI", size))
    return tk.Label(
        parent,
        text=text,
        font=font,
        bg=BG_CARD,
        fg=FG_SECONDARY if secondary else FG_PRIMARY,
    )


def make_entry(parent, width=36):
    frame = tk.Frame(parent, bg=BORDER, bd=0)
    e = tk.Entry(
        frame,
        width=width,
        font=FONT_BODY,
        bg=BG_INPUT,
        fg=FG_PRIMARY,
        insertbackground=FG_PRIMARY,
        relief="flat",
        bd=8,
        highlightthickness=0,
    )
    e.pack(fill="x")
    return frame, e


def make_separator(parent):
    return tk.Frame(parent, bg=BORDER, height=1)


def make_badge(parent, text, color=ACCENT):
    return tk.Label(
        parent,
        text=f"  {text}  ",
        font=FONT_SMALL,
        bg=color,
        fg="#FFFFFF",
        padx=4,
        pady=2,
        relief="flat",
    )

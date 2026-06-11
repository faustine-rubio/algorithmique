import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random

from data.vocab_data import vocab, load_all_vocab
from scores.scores import set_best_score

ROWS = 4
COLS = 4
CARD_BACK = "❓"


def open_memory_game():
    if not vocab:
        load_all_vocab()

    vocab_items = [
        (french, value[0])
        for french, value in vocab.items()
        if value and value[0]
    ]
    total_cards = ROWS * COLS
    total_pairs = total_cards // 2

    if len(vocab_items) < total_pairs:
        messagebox.showerror(
            "Memory",
            f"Pas assez de mots dans le vocabulaire pour lancer le jeu ({total_pairs} paires requises)."
        )
        return

    selected_pairs = random.sample(vocab_items, total_pairs)
    card_data = []
    for pair_id, (french, english) in enumerate(selected_pairs):
        card_data.append((french, pair_id))
        card_data.append((english, pair_id))

    random.shuffle(card_data)
    cards = [text for text, _ in card_data]
    pair_ids = [pair_id for _, pair_id in card_data]

    window = tk.Toplevel()
    window.title("Memory Game")
    window.geometry("500x450")
    window.resizable(False, False)
    window.config(bg="#eef5ff")


    title = tk.Label(
        window,
        text="Memory",
        font=("Comic Sans MS", 24, "bold"),
        bg="#eef5ff",
        fg="#1a3c7a"
    )
    title.pack(pady=10)

    board_frame = tk.Frame(window, bg="#eef5ff")
    board_frame.pack(padx=10, pady=10)

    status_frame = tk.Frame(window, bg="#eef5ff")
    status_frame.pack(fill="x", padx=10)

    bottom_frame = tk.Frame(window, bg="#eef5ff")
    bottom_frame.pack(fill="x", padx=10, pady=10)

    moves_var = tk.IntVar(value=0)
    revealed = [False] * (ROWS * COLS)
    buttons = [None] * (ROWS * COLS)
    first_choice = None
    second_choice = None
    busy = False

    def check_match():
        nonlocal first_choice, second_choice, busy

        if pair_ids[first_choice] == pair_ids[second_choice] and first_choice != second_choice:
            revealed[first_choice] = True
            revealed[second_choice] = True
        else:
            buttons[first_choice].config(text=CARD_BACK, state="normal")
            buttons[second_choice].config(text=CARD_BACK, state="normal")

        first_choice = None
        second_choice = None
        busy = False

        if all(revealed):
            moves = moves_var.get()

            # score basé sur efficacité (plus tu fais peu de coups, meilleur score)
            score = max(0, total_pairs * 10 - moves)

            set_best_score("memory", score)
            window.event_generate("<<BestScoreChanged>>")

            messagebox.showinfo(
                "Victory",
                f"Congratulations! You won in {moves} moves.\nScore : {score}",
                parent=window
            )

            window.destroy()

    def on_card_click(index):
        nonlocal first_choice, second_choice, busy

        if busy or revealed[index] or index == first_choice:
            return

        buttons[index].config(text=cards[index], state="disabled")

        if first_choice is None:
            first_choice = index
            return

        second_choice = index
        moves_var.set(moves_var.get() + 1)
        busy = True
        window.after(800, check_match)

    moves_label = tk.Label(
        status_frame,
        text="Moves :",
        font=("Arial", 12, "bold"),
        bg="#eef5ff",
        fg="#2b4c7a"
    )

    moves_value_label = tk.Label(
        status_frame,
        textvariable=moves_var,
        font=("Arial", 12),
        bg="#eef5ff",
        fg="#2b4c7a"
    )

    moves_label.pack(side="left")
    moves_value_label.pack(side="left", padx=5)

    for index in range(ROWS * COLS):
        button = ttk.Button(
            board_frame,
            text=CARD_BACK,
            width=12,
            command=lambda i=index: on_card_click(i)
        )
        button.grid(row=index // COLS, column=index % COLS, padx=4, pady=4)
        buttons[index] = button

    quit_button = ttk.Button(
        bottom_frame,
        text="Exit",
        command=window.destroy
    )
    quit_button.pack(side="right")

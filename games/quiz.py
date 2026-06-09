import tkinter as tk
from tkinter import ttk
import random

from data.vocab_data import vocab


def open_quiz():
    # crée une fenêtre Tk principale si nécessaire
    if tk._default_root is None:
        window = tk.Tk()
        own_root = True
    else:
        window = tk.Toplevel()
        own_root = False

    window.title("Quiz")
    window.geometry("500x320")
    window.resizable(False, False)

    # paramètres du quiz
    score = 0
    question_index = 0
    nb_questions = 5

    # construire la liste de mots français disponibles
    french_words = list(vocab.keys())
    if not french_words:
        tk.messagebox.showinfo("Quiz", "Le vocabulaire est vide. Ajoutez des mots d'abord.")
        if own_root:
            window.destroy()
        return

    # nombre de questions limité par le nombre de mots disponibles
    nb_questions = min(nb_questions, len(french_words))

    # sélectionner des mots aléatoires sans répétition
    selected = random.sample(french_words, nb_questions)

    # Titre
    title = tk.Label(window, text="Quiz", font=("Arial", 18, "bold"))
    title.pack(pady=12)

    content_frame = tk.Frame(window)
    content_frame.pack(fill="both", expand=True, padx=16)

    score_label = tk.Label(content_frame, text=f"Score : {score}", font=("Arial", 12))
    score_label.pack(pady=4)

    question_label = tk.Label(content_frame, text="")
    question_label.pack()

    instruction_label = tk.Label(content_frame, text="Traduisez en anglais :", font=("Arial", 12))
    instruction_label.pack()

    word_label = tk.Label(content_frame, text="", font=("Arial", 16, "bold"))
    word_label.pack(pady=8)

    answer_entry = tk.Entry(content_frame, font=("Arial", 12))
    answer_entry.pack(pady=6)

    result_label = tk.Label(content_frame, text="")
    result_label.pack(pady=6)

    def afficher_question():
        nonlocal question_index
        if question_index < nb_questions:
            french = selected[question_index]
            word_label.config(text=french)
            question_label.config(text=f"Question {question_index+1}/{nb_questions}")
            answer_entry.config(state="normal")
            answer_entry.delete(0, tk.END)
            result_label.config(text="")
        else:
            word_label.config(text="Quiz terminé !")
            result_label.config(text=f"Score final : {score}/{nb_questions}")
            validate_button.config(state="disabled")
            answer_entry.config(state="disabled")

    def verifier_reponse():
        nonlocal score, question_index
        if question_index >= nb_questions:
            return

        user = answer_entry.get().strip().lower()
        french = selected[question_index]
        correct = vocab.get(french)
        correct_answer = correct[0].lower() if correct and isinstance(correct, (list, tuple)) and len(correct) >= 1 else ""

        if user == correct_answer:
            score += 1
            result_label.config(text="✅ Bonne réponse !")
        else:
            result_label.config(text=f"❌ Faux ! Réponse : {correct_answer}")

        score_label.config(text=f"Score : {score}")
        question_index += 1
        # attendre un court instant puis afficher la question suivante
        window.after(800, afficher_question)

    buttons_frame = tk.Frame(content_frame)
    buttons_frame.pack(pady=8)

    validate_button = ttk.Button(buttons_frame, text="Valider", command=verifier_reponse)
    validate_button.pack(side="left", padx=6)

    quit_button = ttk.Button(buttons_frame, text="Quitter", command=window.destroy)
    quit_button.pack(side="left", padx=6)

    afficher_question()

    if own_root:
        window.mainloop()


if __name__ == "__main__":
    open_quiz()
    buttons_frame = tk.Frame(content_frame)
    buttons_frame.pack(pady=10)

    validate_button = ttk.Button(
        buttons_frame,
        text="Valider",
        command=verifier_reponse
    )
    validate_button.pack(side="left", padx=5)

    quit_button = ttk.Button(
        buttons_frame,
        text="Quitter",
        command=window.destroy
    )
    quit_button.pack(side="left", padx=5)

    # Première question
    afficher_question()

    if own_root:
        window.mainloop()


if __name__ == "__main__":
    open_quiz()

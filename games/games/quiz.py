import tkinter as tk
from tkinter import ttk
import random


def open_quiz():
    if tk._default_root is None:
        window = tk.Tk()
        own_root = True
    else:
        window = tk.Toplevel()
        own_root = False

    window.title("Quiz")
    window.geometry("500x300")
    window.resizable(False, False)

    # Dictionnaire de vocabulaire
    vocab = {
        "apple": "pomme",
        "truck": "camion",
        "house": "maison",
        "dog": "chien",
        "cat": "chat",
        "book": "livre",
        "car": "voiture",
        "tree": "arbre"
    }

    score = 0
    question = 0
    nb_questions = 5

    mots = list(vocab.keys())
    random.shuffle(mots)

    # Titre
    title = tk.Label(
        window,
        text="Quiz",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=20)

    # Espace pour le quiz
    content_frame = tk.Frame(window)
    content_frame.pack(side="top", fill="both", expand=True)

    # Score
    score_label = tk.Label(
        content_frame,
        text="Score : 0",
        font=("Arial", 12)
    )
    score_label.pack(pady=5)

    # Numéro de question
    question_label = tk.Label(content_frame, text="")
    question_label.pack()

    # Mot à traduire
    word_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 16, "bold")
    )
    word_label.pack(pady=10)

    # Zone de saisie
    answer_entry = tk.Entry(content_frame, font=("Arial", 12))
    answer_entry.pack(pady=5)

    # Message résultat
    result_label = tk.Label(content_frame, text="")
    result_label.pack(pady=5)

    def afficher_question():
        nonlocal question

        if question < nb_questions:
            word_label.config(text=mots[question])
            question_label.config(
                text=f"Question {question + 1}/{nb_questions}"
            )
            answer_entry.delete(0, tk.END)
        else:
            word_label.config(text="Quiz terminé !")
            result_label.config(
                text=f"Score final : {score}/{nb_questions}"
            )
            validate_button.config(state="disabled")
            answer_entry.config(state="disabled")

    def verifier_reponse():
        nonlocal score, question

        reponse = answer_entry.get().strip().lower()
        bonne_reponse = vocab[mots[question]].lower()

        if reponse == bonne_reponse:
            score += 1
            result_label.config(text="✅ Bonne réponse !")
        else:
            result_label.config(
                text=f"❌ Faux ! Réponse : {bonne_reponse}"
            )

        score_label.config(text=f"Score : {score}")
        question += 1
        window.after(1000, afficher_question)

    # Boutons Valider et Quitter
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

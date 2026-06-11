import random
import tkinter as tk

from data.vocab_data import vocab
from scores.scores import set_best_score


def open_reverse_translation():
    """Ouvre une fenêtre de quiz EN → FR."""
    if tk._default_root is None:
        window = tk.Tk()
        own_root = True
    else:
        window = tk.Toplevel()
        own_root = False

    window.title("Quiz (EN -> FR)")
    window.geometry("500x320")
    window.resizable(False, False)
    window.config(bg="#eef5ff")

    score = 0
    question_index = 0
    nb_questions = 5

    word_pairs = [(french, data[0]) for french, data in vocab.items() if data and len(data) >= 1]
    if not word_pairs:
        tk.messagebox.showinfo("Quiz (EN -> FR)", "Le vocabulaire est vide. Ajoutez des mots d'abord.")
        if own_root:
            window.destroy()
        return

    nb_questions = min(nb_questions, len(word_pairs))
    selected = random.sample(word_pairs, nb_questions)

    title = tk.Label(
        window,
        text="Quiz (EN -> FR)",
        font=("Comic Sans MS", 24, "bold"),
        bg="#eef5ff",
        fg="#1a3c7a",
    )
    title.pack(pady=12)

    content_frame = tk.Frame(window, bg="#eef5ff")
    content_frame.pack(fill="both", expand=True, padx=16)

    score_label = tk.Label(
        content_frame,
        text=f"Score : {score}",
        font=("Arial", 12, "bold"),
        bg="#eef5ff",
        fg="#2b4c7a",
    )
    score_label.pack(pady=4)

    question_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#eef5ff",
        fg="#2b4c7a",
    )
    question_label.pack()

    instruction_label = tk.Label(
        content_frame,
        text="Traduisez en français :",
        font=("Arial", 12),
        bg="#eef5ff",
        fg="#2b4c7a",
    )
    instruction_label.pack()

    word_label = tk.Label(
        content_frame,
        text="",
        font=("Courier", 24, "bold"),
        bg="#eef5ff",
        fg="#333333",
    )
    word_label.pack(pady=8)

    answer_entry = tk.Entry(content_frame, font=("Arial", 12))
    answer_entry.pack(pady=6)

    result_label = tk.Label(
        content_frame,
        text="",
        font=("Arial", 12, "bold"),
        bg="#eef5ff",
    )
    result_label.pack(pady=6)

    def afficher_question():
        nonlocal question_index

        if question_index < nb_questions:
            french, english = selected[question_index]
            word_label.config(text=english)
            question_label.config(text=f"Question {question_index + 1}/{nb_questions}")
            answer_entry.config(state="normal")
            answer_entry.delete(0, tk.END)
            result_label.config(text="")
        else:
            word_label.config(text="Quiz terminé !")
            result_label.config(text=f"Score final : {score}/{nb_questions}")
            validate_button.config(state="disabled")
            answer_entry.config(state="disabled")
            set_best_score("en-fr", score)

    def verifier_reponse():
        nonlocal score, question_index

        if question_index >= nb_questions:
            return

        user = answer_entry.get().strip().lower()
        french, _english = selected[question_index]
        correct_answer = french.lower()

        if user == correct_answer:
            score += 1
            result_label.config(text="✅ Bonne réponse !", fg="#0a8f3c")
        else:
            result_label.config(text=f"❌ Faux ! Réponse : {french}", fg="#ce2f2f")

        score_label.config(text=f"Score : {score}")
        question_index += 1
        window.after(800, afficher_question)

    buttons_frame = tk.Frame(content_frame, bg="#eef5ff")
    buttons_frame.pack(pady=8)

    validate_button = tk.Button(
        buttons_frame,
        text="Valider",
        command=verifier_reponse,
        font=("Arial", 11, "bold"),
        bg="#4a90e2",
        fg="white",
    )
    validate_button.pack(side="left", padx=6)

    quit_button = tk.Button(
        buttons_frame,
        text="Quitter",
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg="#e74c3c",
        fg="white",
    )
    quit_button.pack(side="left", padx=6)

    afficher_question()

    if own_root:
        window.mainloop()


if __name__ == "__main__":
    open_reverse_translation()

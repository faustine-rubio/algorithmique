import random
import tkinter as tk
from tkinter import ttk
from data.vocab_data import vocab, load_all_vocab
from scores.scores import set_best_score


def open_hangman():
    window = tk.Tk()
    window.title("Jeu du pendu")
    window.geometry("700x460")
    window.resizable(False, False)
    window.config(bg="#eef5ff")

    def choose_word():
        # s'assurer que le vocab est chargé
        if not vocab:
            try:
                load_all_vocab()
            except Exception:
                pass
        # construire un mapping anglais -> français à partir du vocab
        eng_to_fr = {data[0]: french for french, data in vocab.items() if data and data[0]}
        # fallback si vocab vide
        if not eng_to_fr:
            eng_to_fr = {
                "apple": "pomme",
                "truck": "camion",
                "house": "maison",
                "dog": "chien",
                "cat": "chat",
                "book": "livre",
                "car": "voiture",
                "tree": "arbre"
            }
        solution = random.choice(list(eng_to_fr.keys()))
        return solution, eng_to_fr

    solution, words = choose_word()
    lettres_trouvees = set()
    tentatives = tk.IntVar(value=7)
    erreurs = tk.IntVar(value=0)

    def get_affichage():
        return " ".join(
            lettre if lettre in lettres_trouvees else "_"
            for lettre in solution
        )

    def draw_hangman():
        canvas.delete("all")
        canvas.create_rectangle(0, 0, 260, 320, fill="#d8e9ff", outline="")
        canvas.create_line(40, 300, 220, 300, width=12, fill="#6b6b6b")
        canvas.create_line(80, 300, 80, 50, width=12, fill="#6b6b6b")
        canvas.create_line(80, 50, 180, 50, width=12, fill="#6b6b6b")
        canvas.create_line(180, 50, 180, 95, width=8, fill="#6b6b6b")

        stage = erreurs.get()
        if stage >= 1:
            canvas.create_oval(155, 95, 205, 145, width=4, outline="#2b2b2b", fill="#f7f5d1")
        if stage >= 2:
            canvas.create_line(180, 145, 180, 215, width=6, fill="#2b2b2b")
        if stage >= 3:
            canvas.create_line(180, 165, 150, 195, width=5, fill="#2b2b2b")
        if stage >= 4:
            canvas.create_line(180, 165, 210, 195, width=5, fill="#2b2b2b")
        if stage >= 5:
            canvas.create_line(180, 215, 155, 255, width=5, fill="#2b2b2b")
        if stage >= 6:
            canvas.create_line(180, 215, 205, 255, width=5, fill="#2b2b2b")
        if stage >= 7:
            canvas.create_oval(168, 110, 175, 117, fill="#2b2b2b", outline="")
            canvas.create_oval(185, 110, 192, 117, fill="#2b2b2b", outline="")
            canvas.create_line(170, 130, 190, 130, width=3, fill="#2b2b2b")

    def refresh_interface(message=""):
        word_label.config(text=get_affichage())
        attempts_label.config(text=f"Tentatives restantes : {tentatives.get()}")
        letters_label.config(text=f"Lettres proposées : {' '.join(sorted(lettres_trouvees))}")
        status_label.config(text=message)
        draw_hangman()

        if "_" not in get_affichage():
            status_label.config(text=">>> Gagné ! <<<", fg="#0a8f3c")
            guess_button.config(state="disabled")
            letter_entry.config(state="disabled")
            try:
                score = tentatives.get()
                
                set_best_score("hangman", score)
                window.event_generate("<<BestScoreChanged>>")
            except Exception:
                pass
        elif tentatives.get() <= 0:
            # montrer aussi la traduction française si disponible
            french = words.get(solution, "")
            if french:
                status_label.config(text=f"Perdu... Le mot était '{solution}' ({french}).", fg="#ce2f2f")
            else:
                status_label.config(text=f"Perdu... Le mot était '{solution}'.", fg="#ce2f2f")
            guess_button.config(state="disabled")
            letter_entry.config(state="disabled")
        # afficher la traduction si il ne reste qu'une tentative et que le mot n'est pas trouvé
        try:
            if tentatives.get() == 1 and "_" in get_affichage():
                french = words.get(solution, "")
                if french:
                    hint_label.config(text=f"Traduction : {french}")
                else:
                    hint_label.config(text="")
            else:
                hint_label.config(text="")
        except Exception:
            try:
                hint_label.config(text="")
            except Exception:
                pass

    def proposer_lettre(event=None):
        lettre = letter_entry.get().strip().lower()[:1]
        letter_entry.delete(0, tk.END)

        if lettre == "":
            refresh_interface("Tape une lettre.")
            return
        if not lettre.isalpha():
            refresh_interface("Veuillez entrer une lettre.")
            return
        if lettre in lettres_trouvees:
            refresh_interface("Lettre déjà proposée.")
            return

        lettres_trouvees.add(lettre)
        if lettre in solution:
            refresh_interface("Bien joué !")
        else:
            erreurs.set(erreurs.get() + 1)
            tentatives.set(max(0, 7 - erreurs.get()))
            refresh_interface("Lettre incorrecte.")

    def nouvelle_partie():
        nonlocal solution, words
        solution, words = choose_word()
        lettres_trouvees.clear()
        erreurs.set(0)
        tentatives.set(7)
        letter_entry.config(state="normal")
        guess_button.config(state="normal")
        status_label.config(fg="#1a3c7a")
        refresh_interface("Nouvelle partie prête !")

    title = tk.Label(window, text="Jeu du pendu", font=("Comic Sans MS", 24, "bold"), bg="#eef5ff", fg="#1a3c7a")
    title.place(x=280, y=10)

    canvas = tk.Canvas(window, width=260, height=320, bg="#d8e9ff", highlightthickness=0)
    canvas.place(x=20, y=80)

    status_label = tk.Label(window, text="Bienvenue !", font=("Arial", 12, "bold"), bg="#eef5ff", fg="#1a3c7a")
    status_label.place(x=280, y=70)

    # label pour afficher un indice (traduction) lorsque ne reste qu'une tentative
    hint_label = tk.Label(window, text="", font=("Arial", 11), bg="#eef5ff", fg="#1a3c7a")
    hint_label.place(x=280, y=100)

    word_label = tk.Label(window, text=get_affichage(), font=("Courier", 28, "bold"), bg="#eef5ff", fg="#333333")
    word_label.place(x=280, y=140)

    attempts_label = tk.Label(window, text=f"Tentatives restantes : {tentatives.get()}", font=("Arial", 12), bg="#eef5ff", fg="#2b4c7a")
    attempts_label.place(x=280, y=220)

    letters_label = tk.Label(window, text="Lettres proposées :", font=("Arial", 12), bg="#eef5ff", fg="#2b4c7a")
    letters_label.place(x=280, y=255)

    letter_entry = ttk.Entry(window, width=5, font=("Arial", 18))
    letter_entry.place(x=330, y=300)
    letter_entry.focus()

    guess_button = tk.Button(window, text="Proposer", command=proposer_lettre, font=("Arial", 11, "bold"), bg="#4a90e2", fg="white", activebackground="#3b77c4", activeforeground="white")
    guess_button.place(x=420, y=298, width=120, height=38)

    restart_button = tk.Button(window, text="Nouvelle partie", command=nouvelle_partie, font=("Arial", 11, "bold"), bg="#66bb6a", fg="white", activebackground="#57a85a")
    restart_button.place(x=280, y=350, width=130, height=40)

    quit_button = tk.Button(window, text="Quitter", command=window.destroy, font=("Arial", 11, "bold"), bg="#e74c3c", fg="white", activebackground="#c0392b")
    quit_button.place(x=430, y=350, width=130, height=40)

    refresh_interface("Bonne chance !")
    window.bind('<Return>', proposer_lettre)
    window.mainloop()


def hangman():
    tentatives = 7
    solution = "apple"
    lettres_trouvees = set()

    print(">> Bienvenue dans le pendu <<")

    while tentatives > 0:
        affichage = " ".join(
            lettre if lettre in lettres_trouvees else "_"
            for lettre in solution
        )
        print(f"\nMot à deviner : {affichage}")
        print(f"Tentatives restantes : {tentatives}")

        proposition = input("Proposez une lettre : ").strip().lower()
        if not proposition:
            print("Aucune lettre saisie, recommencez.")
            continue

        if proposition in lettres_trouvees:
            print("Vous avez déjà proposé cette lettre.")
            continue

        lettres_trouvees.add(proposition)

        if proposition in solution:
            print("-> Bien vu !")
        else:
            tentatives -= 1
            print("-> Nope\n")

        if all(lettre in lettres_trouvees for lettre in solution):
            affichage = " ".join(
                lettre if lettre in lettres_trouvees else "_"
                for lettre in solution
            )
            print(f"\nMot à deviner : {affichage}")
            print(">>> Gagné ! <<<")
            break

    else:
        print("\nVous avez perdu...")

    print("\n    * Fin de la partie *    ")
    print("Le mot était :", solution)
    return affichage


if __name__ == "__main__":
    open_hangman()
    

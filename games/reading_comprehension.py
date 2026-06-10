import tkinter as tk
from tkinter import ttk
from scores.scores import set_best_score

def open_reading_comprehension():
    window = tk.Toplevel()
    window.title("Compréhension de texte ")
    window.geometry("500x500")
    window.resizable(True, True)

    #Zone défilante
    canvas = tk.Canvas(window)
    scrollbar = ttk.Scrollbar(
        window, 
        orient="vertical", 
        command=canvas.yview
        ) 
    
    canvas.configure(
        yscrollcommand=scrollbar.set
        )
    
    scrollbar.pack(
        side="right",
        fill="y"
        )
    
    canvas.pack(
        side="top",
        fill="both",
        expand=True
        )

    content_frame = tk.Frame(canvas)
    canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
        )

    def on_mousewheel(event):
        if event.delta:
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            canvas.yview_scroll(1, "units")

    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    canvas.bind("<Button-4>", on_mousewheel)
    canvas.bind("<Button-5>", on_mousewheel)
    
    content_frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

    # Titre
    title = tk.Label(
        content_frame,
        text="Compréhension de texte ",
        font=("Arial", 18, "bold")
    )
    title.pack(pady=(10, 5), anchor="w")

    subtitle = tk.Label(
        content_frame,
        text="A Visit to the Science Museum",
        font=("Arial", 12, "italic"),
        fg="gray20"
    )
    subtitle.pack(pady=(0, 15), anchor="w")

    # Frame pour aligner le bouton en bas à droite
    bottom_frame = tk.Frame(window)
    bottom_frame.pack(side="bottom", fill="x")

    result_label = tk.Label(
        bottom_frame,
        text="",
        font=("Arial", 11)
    )
    result_label.pack(side="left", padx=10, pady=10)

    quit_button = ttk.Button(
        bottom_frame,
        text="Quitter",
        command=window.destroy
    )
    quit_button.pack(side="right", padx=15, pady=15)    

    submit_button = ttk.Button(
        bottom_frame,
        text="Valider",
        command=lambda: calculate_score()
    )
    submit_button.pack(side="right", padx=5, pady=15)

    reset_button = ttk.Button(
        bottom_frame,
        text="Recommencer",
        command=lambda: reset_quiz()
    )
    reset_button.pack(side="right", padx=5, pady=15)



    # choix unique par question
    choice_vars = [tk.IntVar(value=0) for _ in range(10)]

    def calculate_score():
        correct_answers = [2, 3, 2, 4, 3, 3, 2, 3, 2, 4]

        score = sum(
            1
            for i, answer in enumerate(correct_answers)
            if choice_vars[i].get() == answer
        )

        result_label.config(text=f"Score: {score} / 10")

        show_feedback(correct_answers)

        # AJOUT IMPORTANT : mise à jour du score global
        set_best_score("reading", score)

    def normalize_text(text):
        if text.endswith(" ✓") or text.endswith(" ✗"):
            return text[:-2]
        return text

    def show_feedback(correct_answers):
        radio_buttons = [
            child for child in content_frame.winfo_children()
            if isinstance(child, tk.Radiobutton)
        ]
        for q_index in range(len(correct_answers)):
            group = radio_buttons[q_index * 4:(q_index + 1) * 4]
            selected_value = choice_vars[q_index].get()
            for button in group:
                text = normalize_text(button.cget("text"))
                button_value = int(button.cget("value"))
                if selected_value != 0 and button_value == selected_value:
                    if selected_value == correct_answers[q_index]:
                        button.config(text=text + " ✓", fg="green")
                    else:
                        button.config(text=text + " ✗", fg="red")
                else:
                    button.config(text=text, fg="black")

    def reset_quiz():
        for var in choice_vars:
            var.set(0)
        result_label.config(text="")
        for child in content_frame.winfo_children():
            if isinstance(child, tk.Radiobutton):
                child.config(text=normalize_text(child.cget("text")), fg="black")

    # Clear any pre-selection at startup
    reset_quiz()

    # Pour mettre le texte
    texte = tk.Label(
        content_frame,
        text="Last Friday, a group of students visited the science museum in their city. They arrived at 9 a.m. with their teacher, Mr. Brown. The museum was large and full of interesting exhibits about space, animals, technology, and the human body. " \
        "The students first watched a short film about the planets in our solar system. They learned many facts about Mars, Jupiter, and Saturn. After that, they explored the technology section, where they could try different interactive activities. Many students enjoyed building simple robots and testing them. " \
        "At noon, the group had lunch in the museum café. Some students ate sandwiches, while others chose pasta or salads. After lunch, they attended a workshop about renewable energy. They learned how solar panels and wind turbines produce electricity. " \
        "Before leaving, the students visited the gift shop. Some bought postcards, while others bought small science kits. They returned to school at 4 p.m. Everyone agreed that the visit was both fun and educational. ",
        font=("Arial",11),
        wraplength=450,
        justify="left"
    )
    texte.pack(anchor="w", fill="x", padx=5, pady=5)

    #Question 1 
    tk.Label(
        content_frame,
        text=" 1. When did the students visit the museum ? "
    ).pack(anchor="w")
    #Réponses
    tk.Radiobutton(
        content_frame,
        text="A. Last Monday",
        variable=choice_vars[0],
        value=1
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="B. Last Friday", #Bonne réponse
        variable=choice_vars[0],
        value=2
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="C. Last Saturday",
        variable=choice_vars[0],
        value=3
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="D. Last Sunday",
        variable=choice_vars[0],
        value=4
    ).pack(anchor="w", padx=10, pady=2)


    #Question  2
    tk.Label(
        content_frame,
        text=" 2. Who accompanied the students ? "
    ).pack(anchor="w")
#Réponse
    tk.Radiobutton(
        content_frame,
        text="A. Their parents",
        variable=choice_vars[1],
        value=1
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="B. Their principal ",
        variable=choice_vars[1],
        value=2
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="C. Their teacher, Mr. Brown", #Bonne réponse
        variable=choice_vars[1],
        value=3
    ).pack(anchor="w", padx=10, pady=2)

    tk.Radiobutton(
        content_frame,
        text="D. Their librarian",
        variable=choice_vars[1],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 3
    tk.Label(
        content_frame,
        text=" 3. What was the first activity at the museum? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Visiting the gift shop",
        variable=choice_vars[2],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Watching a film about planets", #Bonne réponse ?
        variable=choice_vars[2],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Building robots",
        variable=choice_vars[2],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Having lunch",
        variable=choice_vars[2],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 4
    tk.Label(
        content_frame,
        text=" 4. Which planet is NOT mentioned in the text? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Mars",
        variable=choice_vars[3],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Jupiter",
        variable=choice_vars[3],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Saturn",
        variable=choice_vars[3],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Venus",
        variable=choice_vars[3],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 5
    tk.Label(
        content_frame,
        text=" 5. What did many students enjoy doing? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Drawing pictures",
        variable=choice_vars[4],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Playing football",
        variable=choice_vars[4],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Building simple robots", # Bonne réponse
        variable=choice_vars[4],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Reading books",
        variable=choice_vars[4],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 6
    tk.Label(
        content_frame,
        text=" 6. Where did the students have lunch? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. In a park",
        variable=choice_vars[5],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. At school",
        variable=choice_vars[5],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. In the museum café", # Bonne réponse 
        variable=choice_vars[5],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. In a restaurant",
        variable=choice_vars[5],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 7
    tk.Label(
        content_frame,
        text=" 7. What was the afternoon workshop about? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Space exploration",
        variable=choice_vars[6],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Renewable energy", # Bonne réponse
        variable=choice_vars[6],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Animal protection",
        variable=choice_vars[6],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Computer programming",
        variable=choice_vars[6],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 8
    tk.Label(
        content_frame,
        text=" 8. What can solar panels and wind turbines produce? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Water",
        variable=choice_vars[7],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Heat",
        variable=choice_vars[7],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Electricity", # Bonne réponse
        variable=choice_vars[7],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Food",
        variable=choice_vars[7],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 9
    tk.Label(
        content_frame,
        text=" 9. What did some students buy before leaving? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Clothes",
        variable=choice_vars[8],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Science kits", # Bonne réponse
        variable=choice_vars[8],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Bicycles",
        variable=choice_vars[8],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. Tickets",
        variable=choice_vars[8],
        value=4
    ).pack(anchor="w", padx=10, pady=2)

    # Question 10
    tk.Label(
        content_frame,
        text=" 10. How did the students feel about the visit? "
    ).pack(anchor="w", pady=(15, 0))
    tk.Radiobutton(
        content_frame,
        text="A. Bored",
        variable=choice_vars[9],
        value=1
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="B. Tired and unhappy",
        variable=choice_vars[9],
        value=2
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="C. Confused",
        variable=choice_vars[9],
        value=3
    ).pack(anchor="w", padx=10, pady=2)
    tk.Radiobutton(
        content_frame,
        text="D. They thought it was fun and educational", # Bonne réponse
        variable=choice_vars[9],
        value=4
    ).pack(anchor="w", padx=10, pady=2)


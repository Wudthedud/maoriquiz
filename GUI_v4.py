import tkinter as tk

class Start:
    """Start screen class for the Maori Quiz Game."""
    def __init__(self, master, start_callback=None):
        """Initializes the start screen with a welcome label and a start button."""
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)
        self.label = tk.Label(self.frame, text="Welcome to the Maori Quiz Game!", font=("Arial", 24))
        self.label.pack(pady=40)
        self.start_button = tk.Button(self.frame, text="Start", font=("Arial", 18), command=start_callback)
        self.start_button.pack(pady=20)

class GameGUI:
    """Game screen class displaying a question and multiple choice answers."""
    def __init__(self, master, question, choices, answer_index, on_next, score, total):
        """Initializes the game screen with a question, multiple choice answer buttons, and score display."""
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)
        self.question_label = tk.Label(self.frame, text=question, font=("Arial", 22))
        self.question_label.pack(pady=(40, 30))
        self.score_label = tk.Label(self.frame, text=f"Score: {score}/{total}", font=("Arial", 16))
        self.score_label.pack(pady=(0, 20))
        self.choice_buttons = []
        self.answer_index = answer_index
        self.answered = False
        self.on_next = on_next
        self.selected_correct = False
        for idx, choice in enumerate(choices):
            btn = tk.Button(self.frame, text=choice, font=("Arial", 18),
                            command=lambda i=idx: self.check_answer(i))
            btn.pack(pady=10, ipadx=20, ipady=5)
            self.choice_buttons.append(btn)
        self.next_button = tk.Button(self.frame, text="Next", font=("Arial", 16), command=self.next_question)
        self.next_button.pack(pady=30)
        self.next_button.pack_forget()

    def check_answer(self, selected_index):
        """Checks if the selected answer is correct and updates button colors."""
        if self.answered:
            return
        self.answered = True
        for idx, btn in enumerate(self.choice_buttons):
            btn.config(state="disabled")
            if idx == self.answer_index:
                btn.config(bg="green", fg="white")
            elif idx == selected_index:
                btn.config(bg="red", fg="white")
        if selected_index == self.answer_index:
            self.selected_correct = True
        self.next_button.pack()

    def next_question(self):
        """Calls the callback to show the next question."""
        self.frame.destroy()
        self.on_next(self.selected_correct)

class GUI:
    """Game application class that initializes the tkinter root window."""
    def __init__(self):
        """Initializes the tkinter root window and quiz state."""
        self.root = tk.Tk()
        self.root.title("Maori Quiz Game")
        self.root.geometry("1080x720")
        self.start_screen = Start(self.root, self.show_game_screen)
        self.game_screen = None
        self.questions = [
            ("What is the Maori word for 'red'?", ["Whero", "Kakariki", "Kowhai", "Kikorangi"], 0),
            ("What is the Maori word for 'green'?", ["Kakariki", "Whero", "Kowhai", "Kikorangi"], 0),
            ("What is the Maori word for 'yellow'?", ["Kowhai", "Whero", "Kakariki", "Kikorangi"], 0),
            ("What is the Maori word for 'blue'?", ["Kikorangi", "Whero", "Kakariki", "Kowhai"], 0),
            ("What is the Maori word for 'black'?", ["Pango", "Ma", "Kikorangi", "Kowhai"], 0),
            ("What is the Maori word for 'white'?", ["Ma", "Pango", "Whero", "Kakariki"], 0),
            ("What is the Maori word for 'brown'?", ["Parauri", "Kakariki", "Ma", "Pango"], 0),
            ("What is the Maori word for 'orange'?", ["Karaka", "Kowhai", "Whero", "Kikorangi"], 0),
            ("What is the Maori word for 'pink'?", ["Mawhero", "Kakariki", "Kowhai", "Kikorangi"], 0),
            ("What is the Maori word for 'purple'?", ["Waiporoporo", "Kakariki", "Kowhai", "Kikorangi"], 0)
        ]
        self.current = 0
        self.score = 0

    def show_game_screen(self):
        """Destroys the start screen and shows the first game question."""
        self.start_screen.frame.destroy()
        self.current = 0
        self.score = 0
        self.show_question()

    def show_question(self, correct_last=None):
        """Shows the next question or final score."""
        if correct_last is not None:
            if correct_last:
                self.score += 1
            self.current += 1
        if self.current < 10:
            q, choices, answer_index = self.questions[self.current]
            self.game_screen = GameGUI(self.root, q, choices, answer_index, self.show_question, self.score, self.current)
        else:
            self.show_final_score()

    def show_final_score(self):
        """Displays the final score to the user."""
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        label = tk.Label(frame, text=f"Quiz Complete!\nYour score: {self.score}/10", font=("Arial", 28))
        label.pack(pady=60)
        quit_btn = tk.Button(frame, text="Quit", font=("Arial", 18), command=self.root.destroy)
        quit_btn.pack(pady=20)

    def run(self):
        """Starts the tkinter main event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

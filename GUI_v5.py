import customtkinter as ctk
from quizengine import Questions

class Start:
    """Start screen class for the Maori Quiz Game."""
    def __init__(self, master, start_callback=None):
        """Initializes the start screen with a welcome label and a start button."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.label = ctk.CTkLabel(self.frame, text="Welcome to the Maori Quiz Game!", font=("Arial", 24))
        self.label.pack(pady=40)
        self.start_button = ctk.CTkButton(self.frame, text="Start", font=("Arial", 18), command=start_callback)
        self.start_button.pack(pady=20)

class GameGUI:
    """Game screen class displaying a question and multiple choice answers."""
    def __init__(self, master, question, choices, answer_index, on_next, score, total):
        """Initializes the game screen with a question, multiple choice answer buttons, and score display."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.question_label = ctk.CTkLabel(self.frame, text=question, font=("Arial", 22))
        self.question_label.pack(pady=(40, 30))
        self.score_label = ctk.CTkLabel(self.frame, text=f"Score: {score}/{total}", font=("Arial", 16))
        self.score_label.pack(pady=(0, 20))
        self.choice_buttons = []
        self.answer_index = answer_index
        self.answered = False
        self.on_next = on_next
        self.selected_correct = False
        for idx, choice in enumerate(choices):
            btn = ctk.CTkButton(self.frame, text=choice, font=("Arial", 18),
                                command=lambda i=idx: self.check_answer(i))
            btn.pack(pady=10, ipadx=20, ipady=5)
            self.choice_buttons.append(btn)
        self.next_button = ctk.CTkButton(self.frame, text="Next", font=("Arial", 16), command=self.next_question)
        self.next_button.pack(pady=30)
        self.next_button.pack_forget()

    def check_answer(self, selected_index):
        """Checks if the selected answer is correct and updates button colors."""
        if self.answered:
            return
        self.answered = True
        for idx, btn in enumerate(self.choice_buttons):
            btn.configure(state="disabled")
            if idx == self.answer_index:
                btn.configure(fg_color="green", text_color="white")
            elif idx == selected_index:
                btn.configure(fg_color="red", text_color="white")
        if selected_index == self.answer_index:
            self.selected_correct = True
        self.next_button.pack()

    def next_question(self):
        """Calls the callback to show the next question."""
        self.frame.destroy()
        self.on_next(self.selected_correct)

class GUI:
    """Game application class that initializes the customtkinter root window."""
    def __init__(self):
        """Initializes the customtkinter root window and quiz state."""
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Maori Quiz Game")
        self.root.geometry("1080x720")
        self.start_screen = Start(self.root, self.show_game_screen)
        self.game_screen = None
        self.questions_engine = Questions("questions.txt")
        self.questions = [
            (q['question'], q['choices'], q['answer_index'])
            for q in self.questions_engine.questions
        ]
        self.current = 0
        self.score = 0
        self.highscore_manager = HighScore()

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
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both")
        label = ctk.CTkLabel(frame, text=f"Quiz Complete!\nYour score: {self.score}/10", font=("Arial", 28))
        label.pack(pady=60)
        # Update high score if necessary
        self.highscore_manager.update_highscore(self.score)
        highscore_label = ctk.CTkLabel(frame, text=f"High score: {self.highscore_manager.get_highscore()}", font=("Arial", 22))
        highscore_label.pack(pady=10)
        quit_btn = ctk.CTkButton(frame, text="Quit", font=("Arial", 18), command=self.root.destroy)
        quit_btn.pack(pady=20)

    def run(self):
        """Starts the customtkinter main event loop."""
        self.root.mainloop()

class HighScore:
    """Handles reading and updating the high score from a text file."""
    def __init__(self, filepath="highscore.txt"):
        """Initializes the HighScore class and loads the current high score."""
        self.filepath = filepath
        self.highscore = self.load_highscore()

    def load_highscore(self):
        """Loads the high score from the file."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def update_highscore(self, score):
        """Updates the high score in the file if the new score is higher."""
        if score > self.highscore:
            self.highscore = score
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(str(score))

    def get_highscore(self):
        """Returns the current high score."""
        return self.highscore

if __name__ == "__main__":
    gui = GUI()
    gui.run()

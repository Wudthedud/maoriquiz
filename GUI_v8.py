import customtkinter as ctk
from quizengine import Questions
from score import HighScore, Score, ScoreExport
import random

class Start:
    """Start screen class for the Maori Quiz Game."""
    def __init__(self, master, start_callback=None):
        """Initializes the start screen with a welcome label, difficulty selection, and a start button."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.label = ctk.CTkLabel(self.frame, text="Welcome to the Maori Quiz Game!", font=("Arial", 24))
        self.label.pack(pady=40)
        self.difficulty = ctk.StringVar(value="easy")
        self.difficulty_label = ctk.CTkLabel(self.frame, text="Select Difficulty:", font=("Arial", 18))
        self.difficulty_label.pack(pady=(10, 0))
        self.easy_radio = ctk.CTkRadioButton(self.frame, text="Easy", variable=self.difficulty, value="easy", font=("Arial", 16))
        self.easy_radio.pack(pady=5)
        self.hard_radio = ctk.CTkRadioButton(self.frame, text="Hard", variable=self.difficulty, value="hard", font=("Arial", 16))
        self.hard_radio.pack(pady=5)
        self.start_button = ctk.CTkButton(self.frame, text="Start", font=("Arial", 18), command=lambda: start_callback(self.difficulty.get()) if start_callback else None)
        self.start_button.pack(pady=20)

class GameGUI:
    """Game screen class displaying a question and multiple choice answers."""
    def __init__(self, master, question, choices, answer_index, on_next, score, total, question_number=1, question_total=10):
        """Initializes the game screen with a question, multiple choice answer buttons, score display, and question progress."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.progress_label = ctk.CTkLabel(self.frame, text=f"Question {question_number} of {question_total}", font=("Arial", 16))
        self.progress_label.pack(pady=(20, 0))
        self.question_label = ctk.CTkLabel(self.frame, text=question, font=("Arial", 22))
        self.question_label.pack(pady=(20, 30))
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
        self.root.iconbitmap("flag.ico")
        self.start_screen = Start(self.root, self.show_game_screen)
        self.game_screen = None
        self.difficulty = "easy"
        self.questions_engine = Questions("questions.txt")
        self.questions = [
            (q['question'], q['choices'], q['answer_index'])
            for q in self.questions_engine.questions
        ]
        self.score_manager = Score()
        self.highscore_manager = HighScore()
        self.export_manager = ScoreExport()
        self.user_answers = []

    def show_game_screen(self, difficulty="easy"):
        """Destroys the start screen and shows the first game question."""
        self.difficulty = difficulty
        self.start_screen.frame.destroy()
        self.score_manager.reset()
        self.user_answers = []
        self.export_manager = ScoreExport()
        self.questions_engine = Questions("questions.txt", difficulty=difficulty) if hasattr(Questions, 'difficulty') else Questions("questions.txt")
        self.questions = []
        for q in self.questions_engine.questions:
            choices = q['choices'][:]
            correct = choices[q['answer_index']]
            random.shuffle(choices)
            answer_index = choices.index(correct)
            self.questions.append((q['question'], choices, answer_index))
        random.shuffle(self.questions)
        self.show_question()

    def show_question(self, correct_last=None):
        """Shows the next question or final score."""
        if correct_last is not None:
            if correct_last:
                self.score_manager.increment_score()
            self.score_manager.next_question()
        if self.score_manager.get_current() < 10:
            q, choices, answer_index = self.questions[self.score_manager.get_current()]
            if self.score_manager.get_current() > 0:
                prev_idx = self.score_manager.get_current() - 1
                prev_q, prev_choices, prev_answer_index = self.questions[prev_idx]
                user_answer = self.last_user_answer
                self.export_manager.add_result(prev_q, prev_choices, user_answer, prev_answer_index)
            self.game_screen = GameGUI(
                self.root, q, choices, answer_index, self._on_next_question,
                self.score_manager.get_score(), self.score_manager.get_current(),
                question_number=self.score_manager.get_current()+1, question_total=10
            )
        else:
            if hasattr(self, 'last_user_answer'):
                prev_idx = self.score_manager.get_current() - 1
                prev_q, prev_choices, prev_answer_index = self.questions[prev_idx]
                self.export_manager.add_result(prev_q, prev_choices, self.last_user_answer, prev_answer_index)
            self.show_final_score()

    def _on_next_question(self, selected_correct):
        if self.game_screen:
            for idx, btn in enumerate(self.game_screen.choice_buttons):
                if btn.cget('state') == 'disabled' and btn.cget('fg_color') in ("green", "red"):
                    self.last_user_answer = idx
                    break
        self.show_question(selected_correct)

    def show_final_score(self):
        """Displays the final score to the user."""
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both")
        label = ctk.CTkLabel(frame, text=f"Quiz Complete!\nYour score: {self.score_manager.get_score()}/10", font=("Arial", 28))
        label.pack(pady=60)
        self.highscore_manager.update_highscore(self.score_manager.get_score())
        highscore_label = ctk.CTkLabel(frame, text=f"High score: {self.highscore_manager.get_highscore()}", font=("Arial", 22))
        highscore_label.pack(pady=10)
        export_btn = ctk.CTkButton(frame, text="Export Results", font=("Arial", 18), command=self.export_results)
        export_btn.pack(pady=10)
        restart_btn = ctk.CTkButton(frame, text="Restart", font=("Arial", 18), command=lambda: self._restart_quiz(frame))
        restart_btn.pack(pady=10)
        quit_btn = ctk.CTkButton(frame, text="Quit", font=("Arial", 18), command=self.root.destroy)
        quit_btn.pack(pady=20)

    def _restart_quiz(self, frame):
        """Destroys the final score frame and restarts the quiz from the start screen."""
        frame.destroy()
        self.start_screen = Start(self.root, self.show_game_screen)
        self.show_game_screen(self.difficulty)

    def export_results(self):
        """Exports the quiz results to a formatted text file."""
        self.export_manager.export(self.score_manager.get_score(), 10)
        # Optionally, show a message or dialog to the user
        export_label = ctk.CTkLabel(self.root, text="Results exported to quiz_results.txt", font=("Arial", 16), text_color="green")
        export_label.place(relx=0.5, rely=0.95, anchor="center")

    def run(self):
        """Starts the customtkinter main event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

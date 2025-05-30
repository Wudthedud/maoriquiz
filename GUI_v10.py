import random
import customtkinter as ctk
from quizengine_v2 import Questions
from score_v2 import HighScore, Score, ScoreExport

class Start:
    """Start screen class for the Maori Quiz Game."""
    def __init__(self, master, start_callback=None, leaderboard=None):
        """Initializes the start screen with a welcome label, leaderboard, difficulty selection, and a start button."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.label = ctk.CTkLabel(self.frame, text="Welcome to the Maori Quiz Game!", font=("Arial", 36))
        self.label.pack(pady=20)
        if leaderboard:
            leaderboard_frame = ctk.CTkFrame(self.frame)
            leaderboard_frame.pack(pady=(0, 20))
            leaderboard_text = "Leaderboard (Top 10):\n"
            leaderboard_text += f"{'#':<3}{'Name':<13}{'Score':<7}{'Difficulty':<10}\n"
            for idx, (score, name, difficulty) in enumerate(leaderboard, 1):
                leaderboard_text += f"{idx:<3}{name[:12]:<13}{score:<7}{difficulty:<10}\n"
            self.leaderboard_label = ctk.CTkLabel(leaderboard_frame, text=leaderboard_text.strip(), font=("Consolas", 15), justify="left")
            self.leaderboard_label.pack(padx=10, pady=10)
        self.difficulty = ctk.StringVar(value="easy")
        diff_frame = ctk.CTkFrame(self.frame)
        diff_frame.pack(pady=(0, 10))
        self.difficulty_label = ctk.CTkLabel(diff_frame, text="Select Difficulty:", font=("Arial", 18))
        self.difficulty_label.grid(row=0, column=0, padx=10, pady=5)
        self.easy_radio = ctk.CTkRadioButton(diff_frame, text="Easy", variable=self.difficulty, value="easy", font=("Arial", 16))
        self.easy_radio.grid(row=0, column=1, padx=10, pady=5)
        self.hard_radio = ctk.CTkRadioButton(diff_frame, text="Hard", variable=self.difficulty, value="hard", font=("Arial", 16))
        self.hard_radio.grid(row=0, column=2, padx=10, pady=5)
        self.start_button = ctk.CTkButton(self.frame, text="Start", font=("Arial", 18), command=lambda: start_callback(self.difficulty.get()) if start_callback else None)
        self.start_button.pack(pady=20)

class GameGUI:
    """Game screen class displaying a question and multiple choice answers or text input for hard mode."""
    def __init__(self, master, question, choices, answer_index, on_next, score, total, question_number=1, question_total=10, mode="easy", answer_checker=None, correct_text=None):
        """Initializes the game screen with a question, multiple choice answer buttons in a 2x2 grid, score display (top left), and question progress (top center)."""
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(expand=True, fill="both")
        self.score_label = ctk.CTkLabel(self.frame, text=f"Score: {score}/{total}", font=("Arial", 16), anchor="w", width=200, justify="left")
        self.score_label.place(relx=0.01, rely=0.01, anchor="nw")
        self.progress_label = ctk.CTkLabel(self.frame, text=f"Question {question_number} of {question_total}", font=("Arial", 18), anchor="center")
        self.progress_label.place(relx=0.5, rely=0.01, anchor="n")
        self.question_label = ctk.CTkLabel(self.frame, text=question, font=("Arial", 32))
        self.question_label.pack(pady=(60, 30))
        self.on_next = on_next
        self.answered = False
        self.selected_correct = False
        self.mode = mode
        self.answer_index = answer_index
        self.answer_checker = answer_checker
        self.correct_text = correct_text
        if mode == "easy":
            self.grid_frame = ctk.CTkFrame(self.frame)
            self.grid_frame.pack(pady=10)
            self.choice_buttons = []
            for idx, choice in enumerate(choices):
                btn = ctk.CTkButton(self.grid_frame, text=choice, font=("Arial", 18), command=lambda i=idx: self.check_answer(i))
                row, col = divmod(idx, 2)
                btn.grid(row=row, column=col, padx=20, pady=10, ipadx=20, ipady=10, sticky="nsew")
                self.choice_buttons.append(btn)
            for i in range(2):
                self.grid_frame.grid_columnconfigure(i, weight=1)
                self.grid_frame.grid_rowconfigure(i, weight=1)
            self.next_button = ctk.CTkButton(self.frame, text="Next", font=("Arial", 16), command=self.next_question)
            self.next_button.pack(pady=30)
            self.next_button.pack_forget()
        else:
            self.entry_var = ctk.StringVar()
            self.entry = ctk.CTkEntry(self.frame, textvariable=self.entry_var, font=("Arial", 28), width=300)
            self.entry.pack(pady=10)
            self.submit_btn = ctk.CTkButton(self.frame, text="Submit", font=("Arial", 16), command=self.check_text_answer)
            self.submit_btn.pack(pady=(0, 10))
            self.error_label = ctk.CTkLabel(self.frame, text="", font=("Arial", 22), text_color="red")
            self.error_label.pack(pady=(0, 10))
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

    def check_text_answer(self):
        """Checks the text input answer for hard mode questions."""
        if self.answered:
            return
        user_input = self.entry_var.get().strip()
        if not user_input:
            self.error_label.configure(text="Please enter an answer.", font=("Arial", 22))
            return
        correct_text = self.correct_text
        if self.answer_checker:
            is_correct = self.answer_checker(user_input, correct_text)
        else:
            is_correct = user_input.lower() == correct_text.lower()
        if is_correct:
            self.error_label.configure(text="Correct!", text_color="green", font=("Arial", 22))
            self.selected_correct = True
        else:
            self.error_label.configure(text=f"Incorrect. Correct answer: {correct_text}", text_color="red", font=("Arial", 22))
        self.answered = True
        self.entry.configure(state="disabled")
        self.submit_btn.configure(state="disabled")
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
        self.highscore_manager = HighScore()
        self.start_screen = Start(self.root, self.show_game_screen, leaderboard=self.highscore_manager.get_leaderboard())
        self.game_screen = None
        self.difficulty = "easy"
        self.questions_engine = Questions("questions.txt")
        self.questions = [
            (q['question'], q['choices'], q['answer_index'])
            for q in self.questions_engine.questions
        ]
        self.score_manager = Score()
        self.export_manager = ScoreExport()
        self.user_answers = []
        self.last_user_answer = None

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
                self.questions_engine.add_result(prev_q, prev_choices, user_answer, prev_answer_index)
            mode = self.difficulty
            answer_checker = None
            correct_text = None
            if mode == "hard":
                import unicodedata
                def normalize(s):
                    return ''.join(c for c in unicodedata.normalize('NFD', s.lower().strip()) if unicodedata.category(c) != 'Mn')
                answer_checker = lambda user_input, correct_answer: normalize(user_input) == normalize(correct_answer)
                correct_text = choices[answer_index]
            self.game_screen = GameGUI(
                self.root, q, choices, answer_index, self._on_next_question,
                self.score_manager.get_score(), self.score_manager.get_current(),
                question_number=self.score_manager.get_current()+1, question_total=10,
                mode=mode, answer_checker=answer_checker, correct_text=correct_text
            )
        else:
            if hasattr(self, 'last_user_answer'):
                prev_idx = self.score_manager.get_current() - 1
                prev_q, prev_choices, prev_answer_index = self.questions[prev_idx]
                self.questions_engine.add_result(prev_q, prev_choices, self.last_user_answer, prev_answer_index)
            self.show_final_score()

    def _on_next_question(self, selected_correct):
        if self.game_screen:
            if hasattr(self.game_screen, 'choice_buttons'):
                for idx, btn in enumerate(self.game_screen.choice_buttons):
                    if btn.cget('state') == 'disabled' and btn.cget('fg_color') in ("green", "red"):
                        self.last_user_answer = idx
                        break
            else:
                # Hard mode: store the text answer (or a sentinel value)
                self.last_user_answer = self.game_screen.entry_var.get() if hasattr(self.game_screen, 'entry_var') else None
        self.show_question(selected_correct)

    def show_final_score(self):
        """Displays the final score to the user and allows entering a name for the high score only if achieved."""
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, fill="both")
        label = ctk.CTkLabel(frame, text=f"Quiz Complete!\nYour score: {self.score_manager.get_score()}/10", font=("Arial", 28))
        label.pack(pady=20)
        leaderboard_frame = ctk.CTkFrame(frame)
        leaderboard_frame.pack(pady=10)
        highscore_label = ctk.CTkLabel(leaderboard_frame, text=self._get_leaderboard_text(), font=("Consolas", 15), justify="left")
        highscore_label.pack(padx=10, pady=10)
        is_new_high = self._is_new_highscore(self.score_manager.get_score())
        name_widgets = []
        if is_new_high:
            name_label = ctk.CTkLabel(frame, text="Enter your name (max 12 chars):", font=("Arial", 18))
            name_label.pack(pady=(10, 0))
            name_widgets.append(name_label)
            name_var = ctk.StringVar()
            name_entry = ctk.CTkEntry(frame, textvariable=name_var, font=("Arial", 16), width=200)
            name_entry.pack(pady=5)
            name_widgets.append(name_entry)
            save_btn = ctk.CTkButton(frame, text="Save High Score", font=("Arial", 16))
            save_btn.pack(pady=(0, 5))
            name_widgets.append(save_btn)
            error_label = ctk.CTkLabel(frame, text="", font=("Arial", 14), text_color="red")
            error_label.pack(pady=(0, 10))
            name_widgets.append(error_label)
            def save_highscore():
                name = name_var.get().strip()
                if not name:
                    error_label.configure(text="Name cannot be empty.")
                    return
                if len(name) > 12:
                    error_label.configure(text="Name must be 12 characters or less.")
                    return
                self.highscore_manager.update_highscore(self.score_manager.get_score(), name, self.difficulty)
                error_label.configure(text="High score saved!", text_color="green")
                highscore_label.configure(text=self._get_leaderboard_text())
            save_btn.configure(command=save_highscore)
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        restart_btn = ctk.CTkButton(btn_frame, text="Restart", font=("Arial", 18), command=lambda: self._restart_quiz(frame))
        restart_btn.pack(side="left", padx=20)
        quit_btn = ctk.CTkButton(btn_frame, text="Quit", font=("Arial", 18), command=self.root.destroy)
        quit_btn.pack(side="left", padx=20)
        export_btn = ctk.CTkButton(frame, text="Export Results", font=("Arial", 16), command=self.export_results)
        export_btn.place(relx=0.01, rely=0.01, anchor="nw")

    def _restart_quiz(self, frame):
        frame.destroy()
        self.highscore_manager.load_highscores()
        self.start_screen = Start(self.root, self.show_game_screen, leaderboard=self.highscore_manager.get_leaderboard())
        self.show_game_screen(self.difficulty)

    def export_results(self):
        """Exports the quiz results to a formatted text file."""
        self.questions_engine.export_results(self.score_manager.get_score(), 10)
        export_label = ctk.CTkLabel(self.root, text="Results exported to quiz_results.txt", font=("Arial", 16), text_color="green")
        export_label.place(relx=0.5, rely=0.95, anchor="center")

    def run(self):
        """Starts the customtkinter main event loop."""
        self.root.mainloop()

    def _is_new_highscore(self, score):
        """Checks if the given score is a new high score."""
        return score > self.highscore_manager.get_highscore()

    def _get_leaderboard_text(self):
        leaderboard = self.highscore_manager.get_leaderboard()
        text = "Leaderboard (Top 10):\n"
        text += f"{'#':<3}{'Name':<13}{'Score':<7}{'Difficulty':<10}\n"
        for idx, (score, name, difficulty) in enumerate(leaderboard, 1):
            text += f"{idx:<3}{name[:12]:<13}{score:<7}{difficulty:<10}\n"
        return text.strip()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

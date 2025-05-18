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
    def __init__(self, master, question, choices, answer_index):
        """Initializes the game screen with a question and multiple choice answer buttons."""
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)
        self.question_label = tk.Label(self.frame, text=question, font=("Arial", 22))
        self.question_label.pack(pady=(40, 30))
        self.choice_buttons = []
        self.answer_index = answer_index
        for idx, choice in enumerate(choices):
            btn = tk.Button(self.frame, text=choice, font=("Arial", 18),
                            command=lambda i=idx: self.check_answer(i))
            btn.pack(pady=10, ipadx=20, ipady=5)
            self.choice_buttons.append(btn)

    def check_answer(self, selected_index):
        """Checks if the selected answer is correct and updates button colors."""
        for idx, btn in enumerate(self.choice_buttons):
            btn.config(state="disabled")
            if idx == self.answer_index:
                btn.config(bg="green", fg="white")
            elif idx == selected_index:
                btn.config(bg="red", fg="white")

class GUI:
    """Game application class that initializes the tkinter root window."""
    def __init__(self):
        """Initializes the tkinter root window."""
        self.root = tk.Tk()
        self.root.title("Maori Quiz Game")
        self.root.geometry("1080x720")
        self.start_screen = Start(self.root, self.show_game_screen)
        self.game_screen = None

    def show_game_screen(self):
        """Destroys the start screen and shows the game screen with a sample question and choices."""
        self.start_screen.frame.destroy()
        question = "What is the Maori word for 'red'?"
        choices = ["Whero", "Kakariki", "Kowhai", "Kikorangi"]
        answer_index = 0
        self.game_screen = GameGUI(self.root, question, choices, answer_index)

    def run(self):
        """Starts the tkinter main event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

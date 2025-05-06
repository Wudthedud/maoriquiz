import tkinter as tk

class GameApp:
    """Game application class that initializes the tkinter root window."""
    def __init__(self):
        """Initializes the tkinter root window."""
        self.root = tk.Tk()
        self.root.title("Maori Quiz Game")
        self.root.geometry("1080x720")

    def run(self):
        """Starts the tkinter main event loop."""
        self.root.mainloop()

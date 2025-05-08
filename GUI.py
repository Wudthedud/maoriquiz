import tkinter as tk

class Start:
    """Start screen class for the Maori Quiz Game."""
    def __init__(self, master):
        """Initializes the start screen with a welcome label and a start button."""
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)
        self.label = tk.Label(self.frame, text="Welcome to the Maori Quiz Game!", font=("Arial", 24))
        self.label.pack(pady=40)
        self.start_button = tk.Button(self.frame, text="Start", font=("Arial", 18))
        self.start_button.pack(pady=20)

class GUI:
    """Game application class that initializes the tkinter root window."""
    def __init__(self):
        """Initializes the tkinter root window."""
        self.root = tk.Tk()
        self.root.title("Maori Quiz Game")
        self.root.geometry("1080x720")
        self.start_screen = Start(self.root)

    def run(self):
        """Starts the tkinter main event loop."""
        self.root.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()

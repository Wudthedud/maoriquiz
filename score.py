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

class Score:
    """Handles the user's current score and question index."""
    def __init__(self):
        """Initializes the score and current question index."""
        self.current = 0
        self.score = 0

    def reset(self):
        """Resets the score and question index."""
        self.current = 0
        self.score = 0

    def increment_score(self):
        """Increments the user's score by 1."""
        self.score += 1

    def next_question(self):
        """Moves to the next question."""
        self.current += 1

    def get_score(self):
        """Returns the current score."""
        return self.score

    def get_current(self):
        """Returns the current question index."""
        return self.current

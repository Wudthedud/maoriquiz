"""High score and score management module for the Maori Quiz Game.

Provides classes for leaderboard, score tracking, and exporting results.
"""


class HighScore:
    """Handle leaderboard storage and retrieval."""

    def __init__(self, filename="highscore.txt"):
        """Initialize the high score manager with a given filename."""
        self.filename = filename
        self.highscores = []
        self.load_highscores()

    def load_highscores(self):
        """Load leaderboard."""
        self.highscores = []
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '|' in line:
                        parts = line.split('|')
                        if len(parts) == 3:
                            score, name, difficulty = parts
                        elif len(parts) == 2:
                            score, name = parts
                            difficulty = 'easy'
                        else:
                            continue
                        self.highscores.append((int(score), name, difficulty))
            self.highscores.sort(reverse=True, key=lambda x: x[0])
            self.highscores = self.highscores[:10]
        except (FileNotFoundError, IOError):
            self.highscores = []

    def update_highscore(self, score, name=None, difficulty='easy'):
        """Update the high score list with a new entry and writes to file."""
        if not name:
            name = "---"
        self.highscores.append((score, name, difficulty))
        self.highscores.sort(reverse=True, key=lambda x: x[0])
        self.highscores = self.highscores[:10]
        with open(self.filename, 'w', encoding='utf-8') as f:
            for s, n, d in self.highscores:
                f.write(f"{s}|{n}|{d}\n")

    def get_highscore(self):
        """Return the highest score from the leaderboard."""
        if self.highscores:
            return self.highscores[0][0]
        return 0

    def get_highscore_name(self):
        """Return the name associated with the highest score."""
        if self.highscores:
            return self.highscores[0][1]
        return "---"

    def get_highscore_difficulty(self):
        """Return the difficulty associated with the highest score."""
        if self.highscores:
            return self.highscores[0][2]
        return "easy"

    def get_leaderboard(self):
        """Return the list of high scores as the leaderboard."""
        return self.highscores


class Score:
    """Handle the user's current score and question index."""

    def __init__(self):
        """Initialize the score and current question index."""
        self.current = 0
        self.score = 0

    def reset(self):
        """Reset the score and question index to zero."""
        self.current = 0
        self.score = 0

    def increment_score(self):
        """Increment the user's score by 1."""
        self.score += 1

    def next_question(self):
        """Move to the next question index."""
        self.current += 1

    def get_score(self):
        """Return the current score value."""
        return self.score

    def get_current(self):
        """Return the current question index."""
        return self.current


class ScoreExport:
    """Handle exporting the quiz results to a formatted text file."""

    def __init__(self, export_path="quiz_results.txt"):
        """Initialize the export path and prepares storage for results."""
        self.export_path = export_path
        self.results = []

    def add_result(self, question, choices, user_answer, correct_index):
        """Add a result for a single question to the export list."""
        correct = user_answer == correct_index
        self.results.append({
            'question': question,
            'choices': choices,
            'user_answer': user_answer,
            'correct_index': correct_index,
            'correct': correct
        })

    def export(self, score, total):
        """Export the results to a formatted text file."""
        with open(self.export_path, 'w', encoding='utf-8') as f:
            f.write(f"Quiz Results\n{'='*40}\n")
            f.write(f"Score: {score}/{total}\n\n")
            for idx, res in enumerate(self.results, 1):
                f.write(f"Q{idx}: {res['question']}\n")
                for i, choice in enumerate(res['choices']):
                    marker = ''
                    if i == res['user_answer']:
                        marker = '<< Your answer'
                    if i == res['correct_index']:
                        marker = (
                            marker + ' (Correct)'
                            if marker else '(Correct)'
                        )
                    f.write(
                        f"   {i+1}. {choice} {marker}\n"
                    )
                f.write(
                    f"Result: {'Correct' if res['correct'] else 'Incorrect'}"
                    f"\n{'-'*30}\n"
                )
            f.write("\nEnd of Results\n")


class ScoreManager:
    """Handle the user's score, lives, and related logic for the quiz game."""

    def __init__(self, max_lives=3):
        """Initialize the score and lives."""
        self.score = 0
        self.max_lives = max_lives
        self.lives = max_lives

    def increment_score(self):
        """Increment the score by 1."""
        self.score += 1

    def lose_life(self):
        """Decrement lives by 1 if possible."""
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self):
        """Return True if the player still has lives left."""
        return self.lives > 0

    def get_score(self):
        """Return the current score."""
        return self.score

    def get_lives(self):
        """Return the current number of lives."""
        return self.lives

    def reset(self):
        """Reset the score and lives to initial values."""
        self.score = 0
        self.lives = self.max_lives

    def get_hearts(self):
        """Return a list of heart image representing current lives."""
        hearts = []
        for i in range(self.max_lives):
            if i < self.lives:
                hearts.append("heart.png")
            else:
                hearts.append("empty_heart.png")
        return hearts

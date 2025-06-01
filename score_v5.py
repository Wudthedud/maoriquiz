class HighScore:
    """Handles high score storage and retrieval, now with player names, difficulty, and top 10 leaderboard."""
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.highscores = []
        self.load_highscores()

    def load_highscores(self):
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
        except Exception:
            self.highscores = []

    def update_highscore(self, score, name=None, difficulty='easy'):
        if not name:
            name = "---"
        self.highscores.append((score, name, difficulty))
        self.highscores.sort(reverse=True, key=lambda x: x[0])
        self.highscores = self.highscores[:10]
        with open(self.filename, 'w', encoding='utf-8') as f:
            for s, n, d in self.highscores:
                f.write(f"{s}|{n}|{d}\n")

    def get_highscore(self):
        if self.highscores:
            return self.highscores[0][0]
        return 0

    def get_highscore_name(self):
        if self.highscores:
            return self.highscores[0][1]
        return "---"

    def get_highscore_difficulty(self):
        if self.highscores:
            return self.highscores[0][2]
        return "easy"

    def get_leaderboard(self):
        return self.highscores

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

class ScoreExport:
    """Handles exporting the quiz results to a formatted text file."""
    def __init__(self, export_path="quiz_results.txt"):
        """Initializes the export path and prepares storage for results."""
        self.export_path = export_path
        self.results = []

    def add_result(self, question, choices, user_answer, correct_index):
        """Adds a result for a single question."""
        correct = (user_answer == correct_index)
        self.results.append({
            'question': question,
            'choices': choices,
            'user_answer': user_answer,
            'correct_index': correct_index,
            'correct': correct
        })

    def export(self, score, total):
        """Exports the results to a formatted text file."""
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
                        marker = marker + ' (Correct)' if marker else '(Correct)'
                    f.write(f"   {i+1}. {choice} {marker}\n")
                f.write(f"Result: {'Correct' if res['correct'] else 'Incorrect'}\n{'-'*30}\n")
            f.write("\nEnd of Results\n")

class ScoreManager:
    """Handles the user's score, lives, and related logic for the quiz game."""
    def __init__(self, max_lives=3):
        """Initializes the score and lives."""
        self.score = 0
        self.max_lives = max_lives
        self.lives = max_lives

    def increment_score(self):
        """Increments the score by 1."""
        self.score += 1

    def lose_life(self):
        """Decrements lives by 1 if possible."""
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self):
        """Returns True if the player still has lives left."""
        return self.lives > 0

    def get_score(self):
        """Returns the current score."""
        return self.score

    def get_lives(self):
        """Returns the current number of lives."""
        return self.lives

    def reset(self):
        """Resets the score and lives to initial values."""
        self.score = 0
        self.lives = self.max_lives

    def get_hearts(self):
        """Returns a list of heart image filenames representing current lives."""
        hearts = []
        for i in range(self.max_lives):
            if i < self.lives:
                hearts.append("heart.png")
            else:
                hearts.append("empty_heart.png")
        return hearts

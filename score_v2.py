class HighScore:
    """Handles high score storage and retrieval, now with player names."""
    def __init__(self, filename="highscore.txt"):
        self.filename = filename
        self.highscore = 0
        self.name = "---"
        self.load_highscore()

    def load_highscore(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                line = f.readline().strip()
                if '|' in line:
                    score, name = line.split('|', 1)
                    self.highscore = int(score)
                    self.name = name
                else:
                    self.highscore = int(line)
                    self.name = "---"
        except Exception:
            self.highscore = 0
            self.name = "---"

    def update_highscore(self, score, name=None):
        if score > self.highscore or (score == self.highscore and name and name != self.name):
            self.highscore = score
            if name:
                self.name = name
            with open(self.filename, 'w', encoding='utf-8') as f:
                f.write(f"{score}|{self.name}")

    def get_highscore(self):
        return self.highscore

    def get_highscore_name(self):
        return self.name

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

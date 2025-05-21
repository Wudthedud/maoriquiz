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

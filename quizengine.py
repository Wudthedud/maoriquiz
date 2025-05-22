class Questions:
    """Handles loading and providing quiz questions from a text file, supporting difficulty filtering."""
    def __init__(self, filepath, difficulty=None):
        """Initializes the Questions class and loads questions from the given file, optionally filtering by difficulty."""
        self.questions = []
        self.index = 0
        self.load_questions(filepath, difficulty)

    def load_questions(self, filepath, difficulty=None):
        """Loads questions from a text file. Each line should be: difficulty|question|choice1|choice2|choice3|choice4|answer_index"""
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split('|')
                if len(parts) >= 7:
                    q_difficulty = parts[0]
                    if difficulty is None or q_difficulty == difficulty:
                        question = parts[1]
                        choices = parts[2:6]
                        answer_index = int(parts[6])
                        self.questions.append({
                            'question': question,
                            'choices': choices,
                            'answer_index': answer_index
                        })

    def next_question(self):
        """Returns the next question and choices, or None if finished."""
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.index += 1
            return q
        return None

    def reset(self):
        """Resets the question index to start over."""
        self.index = 0

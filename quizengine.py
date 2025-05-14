class Questions:
    """Handles loading and providing quiz questions from a text file."""
    def __init__(self, filepath):
        """Initializes the Questions class and loads questions from the given file."""
        self.questions = []
        self.index = 0
        self.load_questions(filepath)

    def load_questions(self, filepath):
        """Loads questions from a text file. Each line should be: question|choice1|choice2|choice3|choice4|answer_index"""
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    question = parts[0]
                    choices = parts[1:5]
                    answer_index = int(parts[5])
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

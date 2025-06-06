"""Quiz engine module.

Loading, managing, and exporting Maori quiz questions
Provides the Questions class for handling question data and results export.
"""
import random


class Questions:
    """Handles loading and providing quiz questions from a text file."""

    def __init__(self, filepath):
        """Initialize the questions  and loads from the given file."""
        self.questions = []
        self.index = 0
        self.load_questions(filepath)
        self.results = []

    def load_questions(self, filepath):
        """Load questions from a text file.

        Each line should be:
        question|choice1|choice2|choice3|choice4|answer_index
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
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

    def add_result(self, question, choices, user_answer, correct_index):
        """Add a result entry for export."""
        self.results.append({
            'question': question,
            'choices': choices,
            'user_answer': user_answer,
            'correct_index': correct_index
        })

    def export_results(self, score, total, filename="quiz_results.txt"):
        """Export the quiz results to a formatted text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Score: {score}/{total}\n\n")
            for idx, result in enumerate(self.results, 1):
                q = result['question']
                choices = result['choices']
                user_ans = result['user_answer']
                correct = result['correct_index']
                f.write(f"Q{idx}: {q}\n")
                for i, choice in enumerate(choices):
                    marker = (
                        "(Your answer)" if i == user_ans else (
                            "(Correct)" if i == correct else ""
                        )
                    )
                    f.write(f"  {chr(65+i)}. {choice} {marker}\n")
                f.write("\n")
        self.results = []

    def next_question(self):
        """Return the next question and choices, or None if finished."""
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.index += 1
            return q
        return None

    def reset(self):
        """Reset the question index and results to start over."""
        self.index = 0
        self.results = []

    def get_all_questions(self):
        """List all questions (question, choices, answer_index)."""
        return [
            (q['question'], q['choices'], q['answer_index'])
            for q in self.questions
        ]

    def shuffle_questions(self):
        """Shuffle the order of the questions."""
        random.shuffle(self.questions)

    def get_question_count(self):
        """Return the number of loaded questions."""
        return len(self.questions)

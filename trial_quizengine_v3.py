import unicodedata

class Questions:
    """Handles loading and providing quiz questions from a text file, supporting difficulty filtering and result export."""
    def __init__(self, filepath, difficulty=None):
        """Initializes the Questions class and loads questions from the given file, optionally filtering by difficulty."""
        self.questions = []
        self.index = 0
        self.load_questions(filepath, difficulty)
        self.results = []

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

    def add_result(self, question, choices, user_answer, correct_index):
        """Adds a result entry for export."""
        self.results.append({
            'question': question,
            'choices': choices,
            'user_answer': user_answer,
            'correct_index': correct_index
        })

    def export_results(self, score, total, filename="quiz_results.txt"):
        """Exports the quiz results to a formatted text file."""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Score: {score}/{total}\n\n")
            for idx, result in enumerate(self.results, 1):
                q = result['question']
                choices = result['choices']
                user_ans = result['user_answer']
                correct = result['correct_index']
                f.write(f"Q{idx}: {q}\n")
                for i, choice in enumerate(choices):
                    marker = "(Your answer)" if i == user_ans else ("(Correct)" if i == correct else "")
                    f.write(f"  {chr(65+i)}. {choice} {marker}\n")
                f.write("\n")
        self.results = []

    def next_question(self):
        """Returns the next question and choices, or None if finished."""
        if self.index < len(self.questions):
            q = self.questions[self.index]
            self.index += 1
            return q
        return None

    def reset(self):
        """Resets the question index and results to start over."""
        self.index = 0
        self.results = []

    def check_text_answer(self, user_input, correct_answer):
        """Checks if the user's text input matches the correct answer, accent-insensitive and case-insensitive."""
        def normalize(s):
            return ''.join(c for c in unicodedata.normalize('NFD', s.lower().strip()) if unicodedata.category(c) != 'Mn')
        if not isinstance(user_input, str):
            return False
        return normalize(user_input) == normalize(correct_answer)

    def hard_mode_trial(self):
        """Runs a CLI trial for hard mode questions with text input and robust answer checking."""
        import sys
        print("Hard Mode Trial: Type your answer for each question. Accents and case are ignored.")
        score = 0
        for idx, q in enumerate(self.questions):
            print(f"Q{idx+1}: {q['question']}")
            user_input = input("Your answer: ").strip()
            correct = q['choices'][q['answer_index']]
            if self.check_text_answer(user_input, correct):
                print("Correct!\n")
                score += 1
            else:
                print(f"Incorrect. Correct answer: {correct}\n")
        print(f"Final Score: {score}/{len(self.questions)}")

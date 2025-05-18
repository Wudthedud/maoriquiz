from quizengine import Questions

if __name__ == "__main__":
    q = Questions("questions.txt")
    q.reset()
    while True:
        question_data = q.next_question()
        if not question_data:
            break
        print(f"Question: {question_data['question']}")
        for idx, choice in enumerate(question_data['choices']):
            print(f"  {idx+1}. {choice}")
        print(f"Answer index: {question_data['answer_index']}")
        print()

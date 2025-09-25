import random
from typing import List, Dict
from config import QUESTIONS_FILE


class QuestionBank:
    def __init__(self) -> None:
        self.questions: List[str] = []
        self.usage_count: Dict[str, int] = {}
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()  # возврат списка строк
        questions_without_spaces = []
        for line in lines:
            cleaned_line = line.strip()
            questions_without_spaces.append(cleaned_line)
        self.questions = questions_without_spaces

        self.usage_count = {}  # словарь для нахождения счётчика по вопросу
        for question in self.questions:
            # создание записей в словаре / счётчик для каждого вопроса
            self.usage_count[question] = 0

    def get_random_questions(self, n: int = 3) -> List[str]:
        selected_questions = random.sample(self.questions, n)
        for question in selected_questions:
            # метод для записи, что вопрос использован
            self.record_usage(question)
        return selected_questions

    def record_usage(self, question: str) -> None:
        cleaned_question = question.strip()
        if cleaned_question not in self.usage_count:
            self.usage_count[cleaned_question] = 0
        self.usage_count[cleaned_question] += 1

    def get_most_used(self) -> List[str]:
        if not self.usage_count:  # пустой ли словарь
            return []
        else:
            # проход по всем значениям в поисках наибольшего числа
            max_count = max(self.usage_count.values())
            most_used_questions = []
            for question, count in self.usage_count.items():
                if count == max_count:
                    most_used_questions.append(question)
        return most_used_questions

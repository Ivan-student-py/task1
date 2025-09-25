import random
from typing import List
from utils.helpers import calculate_golden_weights


class Student:
    def __init__(self, name: str, gender: str) -> None:
        self.name = name
        self.gender = gender

    def answer_question(self, question: str) -> str:
        words = question.strip().split()
        weights = calculate_golden_weights(words, self.gender)
        return random.choices(words, weights=weights, k=1)[0]

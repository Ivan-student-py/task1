import time
import random
import threading
from typing import List, Dict, Optional, TYPE_CHECKING
from config import (
    WHEN_CAN_BE_BREAK, BREAK_TIME_MIN, BREAK_TIME_MAX,
    MOOD_BAD, MOOD_GOOD
)
from utils.helpers import calculate_golden_weights

# для избежания циклического импорта
if TYPE_CHECKING:
    from .student import Student
    from .question_bank import QuestionBank


class Examiner(threading.Thread):
    def __init__(
        self,
        name: str,
        gender: str,
        # опиональные параметры
        lock: Optional[threading.Lock] = None,
        student_queue: Optional[List['Student']] = None,
        exam_start_time: Optional[float] = None,
        question_bank: Optional['QuestionBank'] = None,
        student_status: Optional[Dict[str, str]] = None,
        student_exam_durations: Optional[Dict[str, float]] = None
    ) -> None:
        # если инициализировать self до super().__init__(), некоторые
        # реализации Python могут не распознать объект как поток
        super().__init__()

        self.name = name
        self.gender = gender
        self.lock = lock
        self.student_queue = student_queue
        self.exam_start_time = exam_start_time
        self.question_bank = question_bank
        self.student_status = student_status
        self.student_exam_durations = student_exam_durations

        self.current_student = None
        self.total_students = 0
        self.failed_count = 0
        self.work_time = 0.0
        self.has_taken_break = False

        self.daemon = False

    def run(self) -> None:  # тело потока экзаменатора
        while True:
            student = None
            with self.lock:
                if self.student_queue:
                    student = self.student_queue.popleft()
            if student is None:
                break

            self.current_student = student
            self.conduct_exam(student)
            self.current_student = None

            if (
                not self.has_taken_break and
                time.time() - self.exam_start_time > WHEN_CAN_BE_BREAK
            ):
                self.has_taken_break = True
                time.sleep(random.uniform(BREAK_TIME_MIN, BREAK_TIME_MAX))

    def conduct_exam(self, student: 'Student') -> None:
        questions = self.question_bank.get_random_questions(3)
        correct_answers = 0
        total_questions = len(questions)
        duration = random.uniform(len(self.name) - 1, len(self.name) + 1)

        for question in questions:
            correct_words = self.generate_correct_answers(question)
            student_answer = student.answer_question(question)
            if student_answer in correct_words:
                correct_answers += 1

        mood_roll = random.random()
        if mood_roll < MOOD_BAD:
            passed = False
        elif mood_roll < MOOD_BAD + MOOD_GOOD:
            passed = True
        else:
            passed = correct_answers > (total_questions - correct_answers)

        self.total_students += 1
        if not passed:
            self.failed_count += 1
        self.work_time += duration

        self.student_status[student.name] = "Passed" if passed else "Failed"
        time.sleep(duration)
        self.student_exam_durations[student.name] = duration

    def generate_correct_answers(self, question: str) -> set:
        words = question.strip().split()
        chosen_word = random.choices(
            words, weights=calculate_golden_weights(words, self.gender))[0]
        correct_set = {chosen_word}
        remaining_words = [w for w in words if w not in correct_set]
        while remaining_words and random.random() < 1 / 3:
            next_word = random.choice(remaining_words)
            correct_set.add(next_word)
            remaining_words.remove(next_word)

        return correct_set

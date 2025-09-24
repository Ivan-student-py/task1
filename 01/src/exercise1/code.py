import time
import random
import threading
# Аннотация типов (tipe hints)
from typing import List, Dict, Optional
# deque
from collections import deque


class Config:
    GOLDEN_SECH = 1.618
    WHEN_CAN_BE_BREAK = 30
    BREAK_TIME_MIN = 12
    BREAK_TIME_MAX = 18
    MOOD_BAD = 1 / 8
    MOOD_GOOD = 1 / 4
    MOOD_NEUTRAL = 5 / 8


def calculate_golden_weights(words: List[str], gender: str) -> List[float]:
    n = len(words)
    weights = [0] * n
    remainder = 1.0
    for i in range(n - 1):
        prob = remainder / Config.GOLDEN_SECH
        if gender == "M":
            weights[i] = prob
        else:
            weights[n - 1 - i] = prob
        remainder -= prob
    if gender == "M":
        weights[n - 1] = remainder
    else:
        weights[0] = remainder
    return weights


# Классы
class Student:
    def __init__(self, name: str, gender: str) -> None:
        self.name = name
        self.gender = gender

    def answer_question(self, question: str) -> str:
        words = question.strip().split()
        weights = calculate_golden_weights(words, self.gender)
        return random.choices(words, weights=weights, k=1)[0]


class Examiner(threading.Thread):
    # изменено
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
                    # Замена pop(0) на popleft()
                    student = self.student_queue.popleft()
            if student is None:
                break

            self.current_student = student
            self.conduct_exam(student)
            self.current_student = None

            if (
                not self.has_taken_break and
                time.time() - self.exam_start_time > Config.WHEN_CAN_BE_BREAK
            ):
                self.has_taken_break = True
                time.sleep(random.uniform(
                    Config.BREAK_TIME_MIN, Config.BREAK_TIME_MAX))

    def conduct_exam(self, student: 'Student') -> None:  # проведение экзамена

        questions = self.question_bank.get_random_questions(3)  # изменено

        correct_answers = 0
        total_questions = len(questions)
        duration = random.uniform(len(self.name) - 1, len(self.name) + 1)

        for question in questions:
            correct_words = self.generate_correct_answers(question)
            student_answer = student.answer_question(question)
            if student_answer in correct_words:
                correct_answers += 1

        mood_roll = random.random()
        if mood_roll < Config.MOOD_BAD:
            passed = False
        elif mood_roll < Config.MOOD_BAD + Config.MOOD_GOOD:
            passed = True
        else:
            passed = correct_answers > (total_questions - correct_answers)

        self.total_students += 1
        if not passed:
            self.failed_count += 1
        self.work_time += duration

        self.student_status[student.name] = "Passed" if passed else "Failed"
        time.sleep(duration)

        # код для лучших студентов
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


class QuestionBank:
    def __init__(self) -> None:
        self.questions: List[str] = []
        self.usage_count: Dict[str, int] = {}
        with open("01/src/exercise1/questions.txt", "r", encoding="utf-8") as f:
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


# Центральный класс


class ExamController:
    def __init__(self) -> None:
        self.students: List[Student] = []
        self.examiners: List[Examiner] = []
        self.students_queue: List[Student] = []
        self.student_status: Dict[str, float] = {}
        # имя студента = длительность экзамена
        self.student_exam_durations: Dict[str, float] = {}
        self.exam_start_time: float = 0.0
        self.lock: Optional[threading.Lock] = None
        self.question_bank: Optional[QuestionBank] = None

    def load_students(self, filename: str = "01/src/exercise1/students.txt") -> None:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.students = []

        # улучшение кода
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line:
                continue
            parts = stripped_line.split()
            name = parts[0]
            gender = parts[1]
            self.students.append(Student(name, gender))
        # начальное состояние
        self.student_status = {
            student.name: "In Queue" for student in self.students}

    # для каждого student в self.students — берётся student.name,
    # кот. становится ключом.

    def load_examiners(self, filename: str = "01/src/exercise1/examiners.txt") -> None:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        self.examiners = []

        # исправление (заглушки)
        for line in lines:
            if not line.strip():  # если строка пустая
                continue
            parts = line.strip().split()
            if len(parts) != 2:
                continue
            name = parts[0]
            gender = parts[1]
            self.examiners.append(Examiner(name, gender))

    def start_exam(self) -> None:
        self.exam_start_time = time.time()
        self.lock = threading.Lock()
        self.question_bank = QuestionBank()
        # общая очередь (deque)
        self.students_queue = deque(self.students)

        self.new_examiners = []

        # объект, у которого уже есть имя и пол
        for old_examiner in self.examiners:

            new_examiner = Examiner(
                name=old_examiner.name,
                gender=old_examiner.gender,
                lock=self.lock,
                student_queue=self.students_queue,  # как в Examiner.__init__
                exam_start_time=self.exam_start_time,
                question_bank=self.question_bank,
                student_status=self.student_status,
                # для лучших студентов
                student_exam_durations=self.student_exam_durations,
            )
            self.new_examiners.append(new_examiner)
        self.examiners = self.new_examiners

        # запуск потоков
        for examiner in self.examiners:
            examiner.start()

        # циклы не должны быть вложенными (застревание)
        while any(examiner.is_alive() for examiner in self.examiners):
            self.display_exam_status()
            time.sleep(0.5)

        for examiner in self.examiners:
            examiner.join()

        self.generate_final_report()

    # метод для рисования таблиц
    def _print_table(self, headers: List[str],
                     rows: List[List], col_widths: List[int]) -> None:
        # Проверка: колонки и ширины совпадают по длине
        if len(headers) != len(col_widths):
            raise ValueError(
                "Number of headers must match number of column widths")

        # Верхняя граница
        border = "+" + "+".join("-" * w for w in col_widths) + "+"
        print(border)

        # Заголовки
        header_row = "|" + "|".join(str(h).ljust(w)
                                    for h, w in zip(headers, col_widths)) + "|"
        print(header_row)

        # Разделитель
        print(border)

        # Строки данных
        for row in rows:
            if len(row) != len(col_widths):
                raise ValueError("Row length must match number of columns")
            row_str = "|" + "|".join(str(cell).ljust(w)
                                     for cell, w in zip(row, col_widths)) + "|"
            print(row_str)

        # Нижняя граница
        print(border)

    # изменено для вывода
    def display_exam_status(self) -> None:
        # ANSI-код: очистить экран и вернуть курсор в начало
        print("\033[2J\033[H", end="")

        # Таблица студентов
        student_data = [(student.name, self.student_status[student.name])
                        for student in self.students]

        # порядок сортировки статусов (словарь приоритетов)
        status_order = {"In Queue": 0, "Passed": 1, "Failed": 2}

        student_data.sort(key=lambda x: status_order[x[1]])

        self._print_table(
            headers=["Student", "Status"],
            rows=student_data,
            col_widths=[12, 10]
        )

        # Подготовка данных для таблицы экзаменаторов (во время экзамена)
        examiner_headers = ["Examiner", "Current student",
                            "Total students", "Failed", "Work time"]
        examiner_rows = []
        for examiner in self.examiners:
            current_student = examiner.current_student.name if examiner.current_student else "-"
            examiner_rows.append([
                examiner.name,
                current_student,
                examiner.total_students,
                examiner.failed_count,
                f"{examiner.work_time:.2f}"
            ])
        self._print_table(examiner_headers, examiner_rows, [13, 17, 17, 9, 14])

        print(
            f"Remaining in queue: {len(self.students_queue)} out of {len(self.students)}"
        )
        print(
            f"Time since exam started: {int(time.time() - self.exam_start_time)} sec")

    def generate_final_report(self) -> None:
        self._clear_screen()
        self._print_final_student_table()
        self._print_final_examiner_table()
        self._print_exam_summary()
        self._print_top_students()
        self._print_top_examiners()
        self._print_best_questions()
        self._print_exam_result()

    def _clear_screen(self) -> None:
        print("\033[2J\033[H", end="")

    def _print_final_student_table(self) -> None:
        student_data = [(s.name,
                         self.student_status[s.name]) for s in self.students]

        status_order = {"Passed": 0, "Failed": 1}
        student_data.sort(key=lambda x: status_order.get(x[1], 999))
        # если ключа нет, вернёт 999;
        # студенты с неизвестным статусом окажутся в конце (защита от ошибок)

        self._print_table(
            headers=["Student", "Status"],
            rows=student_data,
            col_widths=[12, 10]
        )

    def _print_final_examiner_table(self) -> None:
        # Подготовка данных для финальной таблицы экзаменаторов
        headers = ["Examiner", "Total students", "Failed", "Work time"]
        rows = [
            [e.name, e.total_students, e.failed_count, f"{e.work_time:.2f}"]
            for e in self.examiners
        ]
        self._print_table(headers, rows, [13, 17, 9, 14])
        print()

    # общее время экзамена
    def _print_exam_summary(self) -> None:
        total_time = time.time() - self.exam_start_time
        print(f"Time from exam start to finish: {total_time:.2f}")
        print()

    def _print_top_students(self) -> None:
        if self.student_exam_durations:
            min_time = min(self.student_exam_durations.values())
            best_students = [
                name for name, t in self.student_exam_durations.items()
                if t == min_time and self.student_status[name] == "Passed"
            ]
            print("Top performing students: " + ", ".join(best_students))
        else:
            print("Top performing students: None")
        print()

    def _print_top_examiners(self) -> None:
        examiner_rates = []
        for e in self.examiners:
            if e.total_students > 0:
                fail_rate = e.failed_count / e.total_students
            else:
                fail_rate = 1.0
            examiner_rates.append((e.name, fail_rate))

        min_rate = min(rate for _, rate in examiner_rates)
        best_examiners = [name for name,
                          rate in examiner_rates if rate == min_rate]
        print("Top examiners: " + ", ".join(best_examiners))
        print()

    def _print_best_questions(self) -> None:
        best_questions = self.question_bank.get_most_used()
        print("Best questions: " + ", ".join(best_questions))
        print()

    def _print_exam_result(self) -> None:
        total_students = len(self.students)
        # для каждого сдавшего выдаёт 1
        passed_students = sum(
            1 for s in self.students if self.student_status[s.name] == "Passed"
        )
        pass_rate = passed_students / total_students

        if pass_rate > 0.85:
            print("Result: Exam passed")
        else:
            print("Result: Exam failed")


if __name__ == "__main__":
    controller = ExamController()
    controller.load_students()
    controller.load_examiners()
    controller.start_exam()

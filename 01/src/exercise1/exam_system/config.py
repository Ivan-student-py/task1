import os

# глобальные переменные
GOLDEN_SECH = 1.618
WHEN_CAN_BE_BREAK = 30
BREAK_TIME_MIN = 12
BREAK_TIME_MAX = 18
MOOD_BAD = 1 / 8
MOOD_GOOD = 1 / 4
MOOD_NEUTRAL = 5 / 8

# пути к файлам
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.txt")
EXAMERS_FILE = os.path.join(DATA_DIR, "examiners.txt")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.txt")

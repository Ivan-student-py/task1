import time
import random
import os
import threading

#Глобальные переменные
golden_sech = 1.618

when_can_be_break = 30
break_time_min = 12
break_time_max = 18

mood_bad = 1/8
mood_good = 1/4
mood_neit = 5/8


#Классы
class Student():
    def __init__(self, name, gender):
        self.name = name
        self.gender = gender

    def answer_question(self, question):
        words = question.strip().split()
        n = len(words)
        weights = [0] * n
        remainder = 1.0
        for i in range(n - 1):
            prob = remainder / golden_sech
            if self.gender == "M":
                weights[i] = prob
            else:
                weights[n - 1 -i] = prob
            remainder -= prob
        if self.gender == "M":
            weights[n - 1] = remainder
        else:
            weights[0] = remainder
        return random.choices(words, weights=weights, k=1)[0]
    
class Examiner(threading.Thread):
    def __init__(self, name, gender, lock, student_queue, exam_start_time):
        self.name = name
        self.gender = gender
        self.student_queue = student_queue
        self.lock = lock 

        self.current_student = None
        self.total_students = 0
        self.failed_count = 0
        self.work_time = 0.0
        self.has_taken_break = False

        self.exam_start_time = exam_start_time

        super().__init__()
        self.daemon = False

    def run(self): #тело потока экзаменатора
        while True:
            student = None
            with self.lock:
                if self.student_queue:
                    student = self.student_queue.pop(0)
            if student is None:
                break
            
            self.current_student = student
            self.conduct_exam(student)
            self.current_student = None

            if not self.has_taken_break and time.time() - self.exam_start_time > when_can_be_break:
                self.has_taken_break = True
                time.sleep(random.uniform(break_time_min, break_time_max))

    def conduct_exam(self, student): #проведение экзамена
#        questions = get_questions_from_bank(count = 3)


        correct_answers = 0
        total_questions = len(questions)
        duration = random.uniform(len(self.name) - 1, len(self.name) + 1)

        for question in questions:
            correct_words = self.generate_correct_answers(question)
            student_answer = student.answer_question(question)
            if student_answer in correct_words:
                correct_answers += 1

        mood_roll = random.random()
        if mood_roll < mood_bad:
            passed = False
        elif mood_roll < mood_bad + mood_good:
            passed = True
        else:
            passed = correct_answers > (total_questions - correct_answers)

        self.total_students += 1
        if not passed:
            self.failed_count += 1
        self.work_time += duration

        student_status[student.name] = 'Passed' if passed else 'Failed'
        time.sleep(duration)

    def get_golden_weights(self,words):
        n = len(words)
        weights = [0] * n
        remainder = 1.0
        for i in range(n - 1):
            prob = remainder / golden_sech
            if self.gender == "M":
                weights[i] = prob
            else:
                weights[n - 1 -i] = prob
            remainder -= prob
        if self.gender == "M":
            weights[n - 1] = remainder
        else:
            weights[0] = remainder
        return weights

    def generate_correct_answers(self, question):
        words = question.strip().split()
        chosen_word = random.choices(words, weights=self.get_golden_weights(words))[0]
        correct_set = {chosen_word}

        remaining_words = [w for w in words if w not in correct_set]
        while remaining_words and random.random() < 1/3:
            next_word = random.choice(remaining_words)
            correct_set.add(next_word)
            remaining_words.remove(next_word)

        return correct_set
    
class QuestionBank():
    def __init__(self):
        with open('questions.txt', 'r', encoding= 'utf-8') as f:
            strings = f.readlines() #возврат списка строк
        questions_without_spaces = []
        for line in strings:
            shorted_line = line.strip()
            questions_without_spaces.append(shorted_line)
        self.questions = questions_without_spaces

        self.usage_count = {} # словарь для нахождения счётчика по вопросу
        for question in self.questions:
            self.usage_count[question] = 0 # создание записей в словаре / счётчик для каждого вопроса
            
    def get_random_questions(self, n=3):
        selected_questions = random.sample(self.questions, n)
        for question in selected_questions:
            self.record_usage(question) #метод для записи, что вопрос использован
        return selected_questions

    def record_usage(self, question):
        cleaned_question = question.strip()
        if cleaned_question not in self.usage_count:
            self.usage_count[cleaned_question] = 0
        self.usage_count[cleaned_question] += 1

    def get_most_used(self):
        if not self.usage_count: #пустой ли словарь
            return []
        else:
            max_count = max(self.usage_count.values()) #проход по всем значениям в поисках наибольшего числа
            most_used_questions = []
# переделаю
            for i in self.usage_count.items(): 
                if i == max_count:
                    most_used_questions.append(i)
        return most_used_questions
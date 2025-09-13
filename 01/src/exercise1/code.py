import asyncore
import time
import random
import os

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
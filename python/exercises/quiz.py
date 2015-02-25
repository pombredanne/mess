import random
import datetime


class Question:
    answer = None
    text = None


class Add(Question):

    def __init__(self, num1, num2):
        self.text = '{} + {}'.format(num1, num2)
        self.answer = num1 * num2


class Quiz:
    questions = []
    answers = []

    def __init__(self):
    	# generate random questions

    def take_quiz(self):
    	#log start, ask questions

    def ask(self, question):
    	pass

    def summary(self):
    	
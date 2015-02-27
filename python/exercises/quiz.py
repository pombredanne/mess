import random
import datetime


class Question:
    answer = None
    text = None


class Add(Question):

    def __init__(self, num1, num2):
        self.text = '{} + {}'.format(num1, num2)
        self.answer = num1 + num2


class Multiply(Question):

    def __init__(self, num1, num2):
        self.test = '{} * {}'.format(num1, num2)
        self.answer = num1 * num2


class Quiz:
    questions = []
    answers = []

    def __init__(self):
        question_types = (Add, Multiply)
        '''
        The above can now be called as:
        question_types[0](1, 5)
        '''
        for _ in range(10):
            num1 = random.randint(1, 10)
            num2 = random.randint(1, 10)
            question = random.choice(question_types)(num1, num2)
            self.questions.append(question)

    def take_quiz(self):
        pass
        # log start, ask questions

    def ask(self, question):
        pass

    def total_correct(self):
        total = 0
        for answer in self.answers:
            if answer[0]:
                total += 1
        return total

    def summary(self):
        print "You got {} out of {} right".format(self.total_correct(), len(self.questions))
        print "It took you {} seconds total".format((self.end_time - self.start_time).seconds)

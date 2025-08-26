# from question_model import Question
# from quiz_data import question_data
from quiz_brain import QuizBrain
from quiz_ui import QuizInterface
from random import shuffle
import pandas as pd
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from tkinter.filedialog import askopenfile
import os

class Question:
    def __init__(self, question: str, correct_answer: str, choices: list):
        self.question_text = question
        self.correct_answer = correct_answer
        self.choices = choices


def Main():

    filepath = open_file()

    if filepath:
 
        question_data = pd.read_excel(filepath)
        # print(question_data)


        question_data = question_data.reset_index()

        question_bank = []
        totalquestion = 0
        for index, row in question_data.iterrows():
            choices = []
            question_text = row["Question"]
            correct_answer = row["Final Answer"]
            choices.append(row["A"])
            choices.append(row["B"])
            choices.append(row["C"])
            choices.append(row["D"])
            shuffle(choices)
            new_question = Question(question_text, correct_answer, choices)
            totalquestion = totalquestion + 1
            # print(question_text, correct_answer, choices)
            question_bank.append(new_question)

        # print(totalquestion)

        # question_bank = []
        # for question in question_data:
        #     print(question)
        #     choices = []
        #     question_text = question_data["Question"]
        #     correct_answer = question_data["Final Answer"]
            
        #     # print(question_text)
        #     # print(correct_answer)

        #     choices.append(question_data["A"])
        #     choices.append(question_data["B"])
        #     choices.append(question_data["C"])
        #     choices.append(question_data["D"])
            
        #     # shuffle(choices)
        #     new_question = Question(question_text, correct_answer, choices)
        #     print(question_text, correct_answer, choices)
        #     question_bank.append(new_question)



        shuffle(question_bank)
        quiz = QuizBrain(question_bank, totalquestion)

        quiz_ui = QuizInterface(quiz)


        print("You've completed the quiz")
        print(f"Your final score was: {quiz.score}/{quiz.question_no}")

    else:
        messagebox.showerror("showerror", "Input File Not selected")

def open_file():
   file = filedialog.askopenfile(mode='r', filetypes=[('Excel', '*.xlsx')])
   print(file)
   if file:
        filepath = os.path.abspath(file.name)
        print(filepath)
        return f"{filepath}"
   



Main()
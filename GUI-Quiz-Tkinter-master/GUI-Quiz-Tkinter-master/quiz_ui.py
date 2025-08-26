from tkinter import Tk, Canvas, StringVar, Label, Radiobutton, Button, messagebox
from quiz_brain import QuizBrain
from tkinter import *
import tkinter as tk

# ***** VARIABLES *****
# use a boolean variable to help control state of time (running or not running)
running = False
# time variables initially set to 0
hours, minutes, seconds = 0, 0, 0

THEME_COLOR = "#375362"


class QuizInterface:

    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("iQuiz App")
        self.window.geometry("1500x900")

        # Display Title
        self.display_title()

        # Creating a canvas for question text, and dsiplay question
        self.canvas = Canvas(width=1500, height=400)
        self.question_text = self.canvas.create_text(750, 100,
                                                     text="Question here",
                                                     width=1400,
                                                     fill=THEME_COLOR,
                                                     font=(
                                                         'Ariel', 18, 'bold')
                                                     )
        self.canvas.grid(row=2, column=0, columnspan=2, pady=60)
        self.display_question()

        # Declare a StringVar to store user's answer
        self.user_answer = StringVar()

        # Display four options(radio buttons)
        self.opts = self.radio_buttons()
        self.display_options()

        # To show whether the answer is correct or wrong
        self.feedback = Label(self.window, pady=10, font=("Ariel", 18, "bold"), wraplength=1400)
        self.feedback.place(x=10, y=700)
        

        # Next and Quit Button
        self.buttons()
        self.display_Totalquestion()

        # label to display time
        
        self.update()
        # # start, pause, reset, quit buttons
        # start_button = Button(text='start', height=5, width=7, font=('Arial', 20), command=start)
        # start_button.pack(side=tk.LEFT)
        
        # def start():
        #     global running
        #     if not running:
        #         self.update()
        #         running = True

        # update stopwatch function
        

        # Mainloop
        self.window.mainloop()


    def update(self):
            # update seconds with (addition) compound assignment operator
            global hours, minutes, seconds
            seconds += 1
            if seconds == 60:
                minutes += 1
                seconds = 0
            if minutes == 60:
                hours += 1
                minutes = 0
            # format time to include leading zeros
            hours_string = f'{hours}' if hours > 9 else f'0{hours}'
            minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
            seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
            # update timer label after 1000 ms (1 second)
            timerupdate = Label(self.window, text= f"{hours_string}:{minutes_string}:{seconds_string}" ,width=10, bg="green", fg="white", font=("ariel", 20, "bold"))
            # after each second (1000 milliseconds), call update function
            # use update_time variable to cancel or pause the time using after_cancel
            global update_time
            update_time = timerupdate.after(1000, self.update)
            
            self.stopwatch_label = timerupdate
            # self.stopwatch_label.pack()
            self.stopwatch_label.place(x=1200, y=2)
    

    def display_title(self):
        """To display title"""

        # Title
        title = Label(self.window, text="iQuiz Application",width=90, bg="green", fg="white", font=("ariel", 20, "bold"))

        # place of the title
        title.place(x=0, y=2)

    def display_question(self):
        """To display the question"""

        q_text = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=q_text)

    def radio_buttons(self):
        """To create four options (radio buttons)"""

        # initialize the list with an empty list of options
        choice_list = []

        # position of the first option
        y_pos = 350

        # adding the options to the list
        while len(choice_list) < 4:

            # setting the radio button properties
            radio_btn = Radiobutton(self.window, text="", variable=self.user_answer,
                                    value='', font=("ariel", 18), width=100,indicatoron=0, wraplength = 1400)

            # adding the button to the list
            choice_list.append(radio_btn)

            # placing the button
            radio_btn.place(x=50, y=y_pos)

            # incrementing the y-axis position by 40
            y_pos += 80

        # return the radio buttons
        return choice_list

    def display_options(self):
        """To display four options"""

        val = 0

        # deselecting the options
        self.user_answer.set(None)

        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in self.quiz.current_question.choices:
            self.opts[val]['text'] = option
            self.opts[val]['value'] = option
            val += 1

    def next_btn(self):
        """To show feedback for each answer and keep checking for more questions"""

        if self.user_answer.get() != "None":
            if self.quiz.check_answer(self.user_answer.get()):
                self.feedback["fg"] = "green"
                self.feedback["text"] = 'Correct answer! \U0001F44D'
            else:
                self.feedback['fg'] = 'red'
                self.feedback['text'] = (f'\U0001F44E The right answer is: {self.quiz.current_question.correct_answer}')

            if self.quiz.has_more_questions():
                # Moves to next to display next question and its options
                self.display_live_result()
                self.display_question()
                self.display_options()
                self.display_Totalquestion()
                
            else:
                # if no more questions, then it displays the score
                self.display_result()

                # destroys the self.window
                self.window.destroy()

        else:
            messagebox.showinfo("Error", "Please select Answer")

    def buttons(self):
        """To show next button and quit button"""

        # The first button is the Next button to move to the
        # next Question
        next_button = Button(self.window, text="Next", command=self.next_btn,
                             width=20, bg="green", fg="white", font=("ariel", 16, "bold"))

        # palcing the button  on the screen
        next_button.place(x=650, y=800)

        # This is the second button which is used to Quit the self.window
        quit_button = Button(self.window, text="Quit", command=self.window.destroy,
                             width=5, bg="red", fg="white", font=("ariel", 12, " bold"))

        # placing the Quit button on the screen
        quit_button.place(x=1400, y=5)

    def display_result(self):
        """To display the result using messagebox"""
        correct, wrong, score_percent = self.quiz.get_score()

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        # calculates the percentage of correct answers
        result = f"Score: {score_percent}%"

        # Shows a message box to display the result
        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

    def display_Totalquestion(self):
        """To display the question"""

        tq_text = self.quiz.question_number()
        newtitle = Label(self.window, text= tq_text ,width=10, bg="green", fg="white", font=("ariel", 20, "bold"))

        # place of the title
        newtitle.place(x=0, y=2)


    def display_live_result(self):
        """To display the result using messagebox"""
        correct, wrong = self.quiz.get_live_score()

        resultpercentage = str(round((correct/(correct + wrong))*100,2)) + "%"

        correct = f"Correct: {correct}"
        wrong = f"Wrong: {wrong}"

        pecentage = Label(self.window, text= f"{resultpercentage}" ,width=10, bg="green", fg="white", font=("ariel", 20, "bold"))
        livescore = Label(self.window, text= f"{correct}" ,width=10, bg="green", fg="white", font=("ariel", 20, "bold"))
        wronglivescore = Label(self.window, text= f"{wrong}" ,width=10, bg="red", fg="white", font=("ariel", 20, "bold"))

        # place of the title
        pecentage.place(x=1200, y=750)
        livescore.place(x=1200, y=800)
        wronglivescore.place(x=1200, y=850)

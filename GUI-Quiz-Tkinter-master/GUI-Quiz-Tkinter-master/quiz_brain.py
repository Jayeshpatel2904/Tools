from tkinter import messagebox

class QuizBrain:

    def __init__(self, questions, totalquestion):
        self.question_no = 0
        self.score = 0
        self.questions = questions
        self.current_question = None
        self.totalquestion = totalquestion


    def has_more_questions(self):
        """To check if the quiz has more questions"""
        
        return self.question_no < len(self.questions)

    def next_question(self):
        """Get the next question by incrementing the question number"""
        
        self.current_question = self.questions[self.question_no]
        self.question_no += 1
        # print("Question: " + str(self.question_no))  
        q_text = self.current_question.question_text
        return f"Q.{self.question_no}: {q_text}"

    def check_answer(self, user_answer):
        """Check the user answer against the correct answer and maintain the score"""
        correct_answer = self.current_question.correct_answer
        # print(str(correct_answer).lower())
        # print(str(user_answer).lower())
        if str(user_answer).lower() == str(correct_answer).lower():
            print(self.score)
            self.score += 1
            return True
        else:
            return False

    def get_score(self):
        """Get the number of correct answers, wrong answers and score percentage."""
        
        wrong = self.question_no - self.score
        score_percent = int(self.score / self.question_no * 100)
        return (self.score, wrong, score_percent)

    def question_number(self):
        """Get the number of correct answers, wrong answers and score percentage."""  
        # print(self.question_no)     
        # print(self.totalquestion)  
        tq_text = str(self.question_no) + " / " + str(self.totalquestion)
        return f"{tq_text}"
    
    def get_live_score(self):
        """Get the number of correct answers, wrong answers and score percentage."""
        
        wrong = self.question_no - self.score
        return (self.score, wrong)
    
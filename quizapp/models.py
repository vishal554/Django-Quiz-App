import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Question(models.Model):
    """
    Question Model that stores the question and 

    some attributes of the question

    **Fields**

    `question_id`: A unique UUID for each question
    `quiz_id`: A foreign Key of the QUIZ model
    `question`: The question text
    `type`: The type of the question (Multiple choice or fill in the blanks)
    `marks_weightage`: The marks this question holds
    `time_weightage`: The time in seconds required to answer this question

    """
    # Model to store the questions
    types = [
        ('MCQ', 'Multiple choice'), 
        ('FIB', 'fill in the blanks')
    ]
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.PROTECT)
    question = models.CharField(max_length=300)
    type = models.CharField(max_length=5, choices=types)
    marks_weightage = models.IntegerField()
    time_weightage = models.FloatField()

    def __str__(self):
        return f'{self.question} : {self.quiz_id.quiz_name}'

    
class FibQuestion(models.Model):
    """
    Model to store the answers of the question 

    of type fill in the blanks

    **Fields**

    'question_id': A foreign Key of the QUESTION model
    'answer': The correct answer for the question

    """
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    answer = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.question_id.question}'

class McqQuestion(models.Model):
    """
    Model to store the answers of the question 

    of type Multiple choice

    **Fields**

    'question_id': A foreign Key of the QUESTION model
    'choice1': the first choice
    'choice2': the second choice
    'choice3': the third choice
    'choice4': the fourth choice
    'answer': The correct answer for the question

    """
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.question_id.question}'

class Quiz(models.Model):
    """
    Model to store the quizes

    **Fields**

    'quiz_id': A unique UUID that is also the primary key
    'quiz_name': A brief title of the quiz
    'quiz_desc': A description about the quiz

    """
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=50)
    quiz_desc = models.CharField(max_length=300)
    

    def __str__(self):
        return f'{self.quiz_name}'

class Taken(models.Model):
    """
    Model which stores the quizes which user

    has completed or has pending

    **Fields**

    'username': Foreign Key to the USER model
    'quiz_id': Foreign Key to the QUIZ model
    'submitted': A flag which tells whether the quiz has been submitted or saved
    'marks_obtained': Marks obtained in the quiz
    'time_taken': Time taken to complete the quiz

    """
    username = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.PROTECT)
    submitted = models.BooleanField()
    marks_obtained = models.IntegerField()
    time_taken = models.IntegerField()
    
    def __str__(self):
        return f'{self.username} - {self.quiz_id.quiz_name} - {self.submitted}'

class UsersAnswer(models.Model):
    """
    Model which stores the quizes which user

    has completed or has pending

    **Fields**

    'username': Foreign Key to the USER model
    'question_id': Foreign Key to the QUESTION model
    'answer': The answer given by the user

    """
    username = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    answer = models.CharField(max_length=50)

    def __str__(self):  
        return f'{self.username} - {self.question_id.question} - {self.answer}'


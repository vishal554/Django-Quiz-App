import uuid
from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Question(models.Model):
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
    # Model to store the Answers of FIB Questions 
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    answer = models.CharField(max_length=100)



class McqQuestion(models.Model):
    # Model to store the choices of MCQ Questions 
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.question_id.question}'

class Quiz(models.Model):
    # Model for quizes
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=50)
    quiz_desc = models.CharField(max_length=300)
    


class Taken(models.Model):
    # Model which stores the quizes taken or ongoing by the user
    username = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.PROTECT)
    submitted = models.BooleanField()
    marks_obtained = models.IntegerField()
    time_taken = models.IntegerField()
    
    def __str__(self):
        return f'{self.username} - {self.quiz_id.quiz_name} - {self.submitted}'

class UsersAnswer(models.Model):
    # Model where the User's answer will be stored
    username = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    question_id = models.ForeignKey("Question", on_delete=models.PROTECT)
    answer = models.CharField(max_length=50)

    def __str__(self):  
        return f'{self.username} - {self.question_id.question} - {self.answer}'


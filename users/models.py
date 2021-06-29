
from django.db import models
from django.db.models.deletion import SET_NULL
from django.db.models.enums import Choices
from Quiz import settings
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

# Create your models here.

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True)
    question = models.CharField(max_length=300)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    Answer = models.CharField(max_length=20)
    weightage = models.IntegerField()

    def __str__(self):
        return f'{self.question_id}'

    

class Quiz(models.Model):
    quiz_id = models.UUIDField(primary_key=True)
    quiz_name = models.CharField(max_length=50)
    question_set = models.JSONField(default=dict)
    total_marks = models.IntegerField()

    def __str__(self):
        return f'{self.quiz_id}'


class Ongoing(models.Model):
    ongoing_id = models.UUIDField(primary_key=True)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    answered = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.ongoing_id}'




class my_user(models.Model):
    username = models.ForeignKey( get_user_model(), on_delete=models.CASCADE)
    ongoing_id = models.ForeignKey('Ongoing', on_delete=models.CASCADE, default='nothing', blank=True, null=True)
    




    




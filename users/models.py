
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

import uuid

from django.contrib.auth import get_user_model

# Create your models here.

class Question(models.Model):
    types = [
        ('MCQ', 'Multiple choice'), 
        ('FIB', 'fill in the blanks')
    ]
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    type = models.CharField(max_length=5, choices=types)
    marks_weightage = models.IntegerField()
    time_weightage = models.FloatField()

    

class FIB_Question(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.CharField(max_length=100)


class MCQ_Question(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)
    answer = models.CharField(max_length=50)


class Quiz(models.Model):
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=50)
    quiz_desc = models.CharField(max_length=300)
    
    def __str__(self):
        return f'{self.quiz_id}'


class Taken(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    submitted = models.BooleanField()
    marks_obtained = models.IntegerField()
    time_taken = models.IntegerField()
    

class users_answer(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.CharField(max_length=50)

    








# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid

from django.contrib.auth import default_app_config, get_user_model

# Create your models here.

class Question(models.Model):
    question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question = models.CharField(max_length=300)
    choice1 = models.CharField(max_length=50)
    choice2 = models.CharField(max_length=50)
    choice3 = models.CharField(max_length=50)
    choice4 = models.CharField(max_length=50)
    type = models.CharField(max_length=10)
    correct_answer = models.CharField(max_length=20)
    marks_weightage = models.IntegerField()
    time_weightage = models.FloatField()

    def __str__(self):
        return f'{self.question_id}'
    

class Quiz(models.Model):
    quiz_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.quiz_id}'


class Ongoing(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    time_used = models.FloatField()
    saved_choices = models.CharField(max_length=50, null=True)


class Taken(models.Model):
    username = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    time_taken = models.FloatField()
    marked_choice = models.CharField(max_length=50, null=True)
    correct_choice = models.CharField(max_length=50)

    





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

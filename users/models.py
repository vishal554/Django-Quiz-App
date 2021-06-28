
from django.db import models

# Create your models here.

class Question(models.Model):
    question_id = models.AutoField
    question = models.CharField(max_length=300)
    choice1 = models.CharField(max_length=200)
    choice2 = models.CharField(max_length=200)
    choice3 = models.CharField(max_length=200)
    choice4 = models.CharField(max_length=200)
    type = models.CharField(max_length=50)
    Answer = models.CharField(max_length=20)
    weightage = models.IntegerField()

    def __str__(self):
        return self.question_id
    

class Quiz(models.Model):
    quiz_id = models.AutoField
    quiz_name = models.CharField(max_length=50)
    question_set = models.JSONField(default=dict)
    total_marks = models.IntegerField()

    def __str__(self):
        return self.quiz_id


class Ongoing(models.Model):
    ongoing_id = models.AutoField
    models.ForeignKey('Quiz', on_delete=models.CASCADE)
    answered = models.JSONField(default=dict)

    def __str__(self):
        return self.ongoing_id


class Taken(models.Model):
    taken_id = models.AutoField
    models.ForeignKey('Quiz', on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()
    
    def __str__(self):
        return self.taken_id


class user(models.Model):
    username = models.ForeignKey('User', on_delete=models.CASCADE)
    taken_id = models.ForeignKey('Taken', on_delete=models.CASCADE)
    ongoing_id = models.ForeignKey('Ongoing', on_delete=models.CASCADE)



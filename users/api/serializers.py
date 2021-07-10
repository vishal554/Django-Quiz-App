from users.models import (
    Quiz,
    Question,
    Taken,
    UsersAnswer,
    FibQuestion,
    McqQuestion
)

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class FibQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FibQuestion
        fields = '__all__'
    

class McqQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqQuestion
        fields = '__all__'


class TakenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taken
        fields = '__all__'


class UsersAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersAnswer
        fields = '__all__'

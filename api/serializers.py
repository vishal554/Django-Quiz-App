from rest_framework.validators import UniqueValidator
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
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user

    

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
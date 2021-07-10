from django.http import response
from rest_framework.authtoken.models import Token
from api.serializers import QuizSerializer, UserSerializer
from users.models import Quiz
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
# Create your views here.

@api_view(['GET',])
def home(request):
    try:
        quizes = Quiz.objects.filter(quiz_name='Artificial Intelligence').get()
    except Quiz.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = QuizSerializer(quizes)
    print(serializer)
    return Response(serializer.data)


@api_view(['POST',])
def register(request):
    serializer = UserSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        print(serializer)
        # user = serializer.save()
        # data['response'] = 'Successfully registered'
        # data['email'] = serializer.email
        # data['username'] = user.username
        # token = Token.objects.get(user=user).key
        # data['token'] = token
        data['serializer'] = serializer
        return redirect('otp_verification')

    else:
        data = serializer.errors
    return Response(data)

    
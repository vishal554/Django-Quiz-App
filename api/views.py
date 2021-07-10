import random
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from api.serializers import QuizSerializer, UserSerializer
from users.models import Quiz
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
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
        data['response'] = 'Success'
        data['email'] = serializer.data['email']
        data['username'] = serializer.data['username']
        data['password'] = request.data['password']
        # token = Token.objects.get(user=user).key
        # data['token'] = token
        
        return Response(data)

    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET',])
def otpverification(request):
    data = {}
    try:
        email = request.GET['email']
        password = request.GET['password']
        username = request.GET['username']
        otp = request.session.get('otp','')
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if otp == '':
        otp = random.randint(11111, 99999)
        request.session['otp'] = otp
        send_mail('OTP Verification',
                    f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
        request.session['otp'] = otp
        request.session['email'] = email
        request.session['password'] = password
        request.session['username'] = username 
        data['response'] = 'Success'
        return Response(data)
    else:
        data['response'] = 'Already sent'
        return Response(data)
    


# @api_view(['POST', ])
# def verify_otp(request):

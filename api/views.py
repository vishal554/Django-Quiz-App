import random
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from api.serializers import FibQuestionSerializer, McqQuestionSerializer, QuestionSerializer, QuizSerializer, TakenSerializer, UserSerializer
from users.models import Quiz, Taken, Question, FibQuestion, McqQuestion, UsersAnswer
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class HomeView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        data = {}
        try:
            Quizes = Quiz.objects.all()
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        username = request.user
        ongoing_quizes = []
        quiz_id_list = []
        taken_quizes = []

        ongoing = Taken.objects.filter(username=username, submitted=False)
        taken = Taken.objects.filter(username=username, submitted=True)

        for i in ongoing:
            ongoing_quizes.append(str(i.quiz_id.quiz_id))

        for i in taken:
            taken_quizes.append(str(i.quiz_id.quiz_id))

        for i in Quizes:
            quiz_id_list.append(str(i.quiz_id))

        for i in list(quiz_id_list):
            if i in ongoing_quizes:
                quiz_id_list.remove(i)
            if i in taken_quizes:
                quiz_id_list.remove(i)

        quizes = []
        for i in quiz_id_list:
            quizes.append(Quiz.objects.get(quiz_id=i))

        ongoings = []
        for i in ongoing_quizes:
            ongoings.append(Quiz.objects.get(quiz_id=i))

        quiz_serializer = QuizSerializer(quizes, many=True)
        ongoing_serializer = QuizSerializer(ongoings, many=True)
        data['quizes'] = quiz_serializer.data
        data['ongoings'] = ongoing_serializer.data

        return Response(data)


class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # user = serializer.save()
            data['response'] = 'Success'
            request.session['email'] = serializer.data['email']
            request.session['username'] = serializer.data['username']
            request.session['password'] = request.data['password']
            # token = Token.objects.get(user=user).key
            # data['token'] = token
            return Response(data)
        else:
            data = serializer.errors
        return Response(data)


class OtpVerificationView(APIView):
    permission_classes = []
    def get(self, request):
        data = {}
        try:
            email = request.session['email']
            password = request.session['password']
            username = request.session['username']
            otp = request.session.get('otp','')
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if otp == '':
            otp = random.randint(11111, 99999)
            request.session['otp'] = otp
            send_mail('OTP Verification',
                        f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
            request.session['otp'] = otp
            print('otp: ', otp)
            data['email'] = email
            data['password'] = password
            data['username'] = username 
            data['response'] = 'Success'
            return Response(data)
        else:
            data['response'] = 'Already sent'
            return Response(data)

    def post(self, request):
        data = {}
        try: 
            email = request.POST['email']
            username = request.POST['username']
            password = request.POST['password']
            entered_otp = request.POST['otp']
            otp = request.session['otp']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if int(otp) == int(entered_otp):
            data['response'] = 'Success'
            data['email'] = email
            data['username'] = username
            request.session['otp'] = ''
            user = User.objects.create(username=username, email=email, password=make_password(password))
            token = Token.objects.get_or_create(user=user)[0]
            print(token)
            data['token'] = token.key
            return Response(data)
        else:
            data['response'] = 'invalid otp'
            return Response(data)


class ProfileView(ListAPIView):
    queryset = Taken.objects.filter(submitted=True)
    serializer_class = TakenSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination


class ResultsView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        marks_weightage = []
        u_answer = []
        correct_answer = []

        try:
            quiz_id = request.POST['quiz_id']
            username = request.user
            question_id = request.POST['question_id']
            last = request.POST['last']
            if request.is_ajax():
                answer = request.POST.get('choice', '')
                time_taken = request.POST['time_remaining']
            else:
                answer = request.POST.get('btnradio', '')
                time_taken = request.POST['time_remaining_input']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        # add the last question to the UsersAnswer Model
        question_instance = Question.objects.filter(
            question_id=question_id).get()

        # check if the answer already exists
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(username=username, question_id=question_instance, answer=answer)

        question_ids = Question.objects.filter(quiz_id=quiz_id)

        # add answers to the questions as empty that user has not attempted
        if last == 'no':
            user_answers = UsersAnswer.objects.filter(username=username)
            user_answered = []
            for i in user_answers:
                user_answered.append(i.question_id)

            for i in question_ids:
                if i not in user_answered:
                    UsersAnswer.objects.create(username=username, question_id=i, answer="")
        
        # Fetch the correct answers and also the answer user has given
        for i in question_ids:
            u_a = UsersAnswer.objects.get(
                username=username, question_id=i.question_id)
            u_answer.append(u_a.answer)
            marks_weightage.append(i.marks_weightage)
            if i.type == "MCQ":
                correct_answer.append(McqQuestion.objects.get(
                    question_id=i.question_id).answer)
            else:
                correct_answer.append(FibQuestion.objects.get(
                    question_id=i.question_id).answer)

        # calculate marks obtained and the percentage
        marks_obt = 0
        for i in range(len(u_answer)):
            if u_answer[i] == correct_answer[i]:
                marks_obt += marks_weightage[i]

        total_marks = sum(marks_weightage)
        perct = ((marks_obt/total_marks) * 100)

        data = {
            'marks_obtained': marks_obt,
            'total_marks': total_marks,
            'percentage': perct,
            'questions': question_ids,
            'UsersAnswer': u_answer,
            'correct_answer': correct_answer,
            'time_taken': time_taken
        }

        quiz_ins = Quiz.objects.get(quiz_id=quiz_id)

        # check if the Taken object already exists or not
        try:
            if Taken.objects.get(username=username, quiz_id=quiz_ins):
                Taken.objects.filter(username=username, quiz_id=quiz_ins).update(
                    marks_obtained=marks_obt, time_taken=time_taken, submitted=True)

        except:
            Taken.objects.create(username=username, quiz_id=quiz_ins,
                                 submitted=True, marks_obtained=marks_obt, time_taken=time_taken)

        return Response(data)


class TakeQuizView(APIView):

    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        continuing = False
        try:
            quiz_id = request.GET['quiz_id']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        question_choice_set, time_limit = get_question_choice_set(quiz_id)
        total_questions = len(list(question_choice_set))

        # check if the user is continuing the quiz
        username = request.user
        user_answers = UsersAnswer.objects.filter(username=username)
        question_ids = Question.objects.filter(quiz_id=quiz_id)
        q_id_list = []

        for i in question_ids:
            q_id_list.append(str(i.question_id))

        for i in user_answers:
            if str(i.question_id.question_id) in q_id_list:
                if i.question_id in list(question_choice_set):
                    del question_choice_set[i.question_id]
                continuing = True

        # If he is continuing then get the remaining time left
        if continuing:
            taken = Taken.objects.get(username=username, quiz_id=quiz_id)
            time_limit = int(taken.time_taken)

        current_question_number = (total_questions - len(list(question_choice_set))) + 1

        try: 
            (question, choices) = next(iter(question_choice_set.items()))
        except:
            return Response(status=status.HTTP_307_TEMPORARY_REDIRECT)

        data = {
            'quiz_id': quiz_id,
            'question': question,
            'choices': choices,
            'time_limit': time_limit,
            'total_questions': total_questions, 
            'current': current_question_number
        }

        if len(list(question_choice_set)) > 1:
            data['last'] = 'no'
            return Response(data)            
        elif len(list(question_choice_set)) == 1:
            data['last'] = 'yes'
            return Response(data)


def get_question_choice_set(quiz_id):
    
    question_set = Question.objects.filter(quiz_id=quiz_id)
    question_choice_set = {}
    time_limit = 0
    for i in question_set:
        time_limit += i.time_weightage
        if i.type == "MCQ":
            question_choice_set[i] = McqQuestion.objects.get(
                question_id=i.question_id)
        elif i.type == "FIB":
            question_choice_set[i] = 'FIB'
    return question_choice_set, time_limit
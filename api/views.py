import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from quizapp.models import Quiz, Taken, Question, UsersAnswer
from api.utils import get_data_of_quiz, get_question_choice_set
from api.serializers import McqQuestionSerializer, QuestionSerializer, QuizSerializer, UserSerializer
# Create your views here.


class HomeView(ListAPIView):
    """
    Home page of the App which shows 

    the available quizes and the ongoing quizes

    **Permissions**

    'TokenAuthentication': A unique token required by the user
                            to access this page
    **Response**

    'data': holds the array of available quizes and ongoings

    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = QuizSerializer
    pagination_class = PageNumberPagination

    
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
    """
    Registers the User but does not add to the 

    User Model yet

    **Permissions**

    'No permission required to access this page'

    **Response**

    'data': Json object which contains the response key and 
            respective values

    """
    permission_classes = []
    authentication_classes = []

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            data['response'] = 'Success'
            data['email'] = serializer.data['email']
            data['username'] = serializer.data['username']
            data['password'] = request.data['password1']
            return Response(data)
        else:
            data['response'] = 'fail'
            data = serializer.errors
        return Response(data)


class OtpVerificationView(APIView):
    """
    Sends the OTP to the user and verifies the OTP

    If the OTP is correct then adds the user to

    the USER model

    **Permissions**

    'No permission required to access this page'

    **Response**

    'data': Json object which contains the response key and 
            respective values

    """
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
            data['response'] = 'OTP sent successfully'
            return Response(data)
        else:
            data['response'] = 'OTP Already sent to your email Id'
            return Response(data)

    def post(self, request):
        data = {}
        try: 
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            entered_otp = request.data['user_otp']
            otp = request.session['otp']
            print('entered', entered_otp)
            print(otp)
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

    """
    Shows the quizes taken by the user and

    also the score and answers given by the user

    **Permissions**

    'TokenAuthentication': A unique token required by the user
                            to access this page

    **Response**

    'data': Json object which contains the response key and 
            respective values

    """
    
    serializer_class = QuizSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        quiz = []
        username = self.request.user
        taken_objects = Taken.objects.filter(username=username, submitted=True)
        for i in taken_objects:
            quiz.append(i.quiz_id)
        return quiz

    def post(self, request):
        quiz_id = request.data['quiz_id']
        username = request.user
        context = get_data_of_quiz(quiz_id, username)
        question = QuestionSerializer(context['questions'], many=True)
        context['questions'] = question.data
        return Response(context)


class TakeQuizView(APIView):
    """ 
    Displays the question to the user along 

    with the options

    **Permissions**

    'TokenAuthentication': A unique token required by the user
                            to access this page

    **Response**

    'data': Json object which contains the Question object
            and the respective choice model

    """
    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        continuing = False
        try:
            quiz_id = request.data['quiz_id']
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

        question_serializer = QuestionSerializer(data['question'])
        if data['choices'] != 'FIB':
            mcq_serializer = McqQuestionSerializer(data['choices'])
            data['choices'] = mcq_serializer.data

        data['question'] = question_serializer.data
        if len(list(question_choice_set)) > 1:
            data['last'] = 'no'
            return Response(data)            
        elif len(list(question_choice_set)) == 1:
            data['last'] = 'yes'
            return Response(data)


class SaveView(APIView):
    """
    Saves the state so that user can login 

    later and continue with the quiz.

    **Permissions**

    'TokenAuthentication': A unique token required by the user
                            to access this page

    **Response**

    'data': Json object which contains response key
            with appropriate message

    """
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}
        # Getting post data
        try:
            username = request.user
            question_id = request.data['question_id']
            answer = request.data.get('choice', '')
            time_remaining = int(request.data['time_remaining'])
            quiz_id = request.data['quiz_id']
            last = request.data.get('last', 'no')
        except:
            data['response'] = 'Failure'
            return Response(data)

        
        # Add the answer to the UsersAnswer model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(
                    username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(
                username=username, question_id=question_instance, answer=answer)

        quiz_id_ins = Quiz.objects.get(quiz_id=quiz_id)

        # check if the question is the last question of the quiz.
        # If it is then submit the quiz
        if last == 'yes':
        
            context = get_data_of_quiz(quiz_id, username)

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins, submitted=False).update(
                        submitted=True, marks_obtained=context['marks_obtained'], time_taken=time_remaining)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=True, marks_obtained=context['marks_obtained'], time_taken=time_remaining)
        else:

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins).update(
                        time_taken=time_remaining)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=False, marks_obtained=0, time_taken=time_remaining)

        
        data['response'] = 'Success'
        return Response(data)


class SubmitView(APIView):
    """
    Submit the Quiz when the user hits

    back button or closes the window 

    or timer runs out

    **Permissions**

    'TokenAuthentication': A unique token required by the user
                            to access this page

    **Response**

    'data': Json object which contains response key
            with appropriate message

    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {}
        try:
            quiz_id = request.data['quiz_id']
            username = request.user
            question_id = request.data['question_id']
            last = request.data['last']
            answer = request.data['choice']
            time_taken = request.data['time_remaining']

        except Exception as e:
            data['errors'] = 'errors'
            print(e)
            return Response(data)

        # add the last question to the UsersAnswer Model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        # check if the answer already exists
        try:
            if(UsersAnswer.objects.get(username=username, question_id=question_instance)):
                UsersAnswer.objects.filter(
                    username=username, question_id=question_instance).update(answer=answer)
        except:
            UsersAnswer.objects.create(
                username=username, question_id=question_instance, answer=answer)

        question_ids = Question.objects.filter(quiz_id=quiz_id)

        # add answers to the questions as empty that user has not attempted
        if last == 'no':
            user_answers_object = UsersAnswer.objects.filter(username=username)
            user_answered_question_id = []
            for object in user_answers_object:
                user_answered_question_id.append(object.question_id)

            for question_id in question_ids:
                if question_id not in user_answered_question_id:
                    UsersAnswer.objects.create(
                        username=username, question_id=question_id, answer="")

        # Fetch the correct answers and also the answer user has given
        quiz_ins = Quiz.objects.get(quiz_id=quiz_id)

        # get context from the function
        data = get_data_of_quiz(quiz_id, username)

        # check if the Taken object already exists or not
        try:
            if Taken.objects.get(username=username, quiz_id=quiz_ins):
                Taken.objects.filter(username=username, quiz_id=quiz_ins).update(
                    marks_obtained=data['marks_obtained'], time_taken=time_taken, submitted=True)

        except:
            Taken.objects.create(username=username, quiz_id=quiz_ins,
                                 submitted=True, marks_obtained=data['marks_obtained'], time_taken=time_taken)
        data['response'] = 'success'
        data['questions'] = ''
        return Response(data)

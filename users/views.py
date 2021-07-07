import json
from django import dispatch
from django.contrib.auth.forms import UserCreationForm
from django.db.models.query_utils import Q
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from users.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
import random
from django.views import View
from .models import *
from django.contrib.auth.hashers import make_password


class Register(View):
    """
    renders the Register page to the User

    **Context**

    ``form``
        instance of UserRegisterForm class

    **Template:**

    :template:`users/register.html`

    """
    template_name = 'users/register.html'

    def get(self, request):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # check if the form is valid or not
        # if it is then send OTP
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            request.session['email'] = email
            request.session['username'] = username

            return redirect('otp_verification')
        return render(request, self.template_name, {'form': form})


class OtpVerification(View):
    """
    renders the OTP Verification page to the User

    **Template:**

    :template:`users/otpverification.html`

    """
    template_name = 'users/otpverification.html'

    def get(self, request):
        sent = False
        try:
            email = request.session['email']
        except:
            return redirect('register')
        if sent == False:
            otp = random.randint(11111, 99999)
            request.session['otp'] = otp
            send_mail('OTP Verification',
                      f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
            messages.success(
                request, f"OTP Successfully sent to {email}. Please check your email!")
            sent = True
        else:
            messages.warning(request, f'Already sent email with OTP')

        return render(request, self.template_name)

    def post(self, request):
        # check the entered OTP and redirect to respective page
        # depending on whether OTP is correct or not
        entered_otp = request.POST["otp"]
        otp = request.session['otp']
        if int(entered_otp) == int(otp):
            form_data = request.session['form_data']
            form = UserCreationForm(form_data)
            if form.is_valid():
                print("Valid Form: ", form_data)
                password = make_password(form_data['password1'])
                User.objects.create(
                    username=form_data['username'], password=password, email=form_data['email'])
                username = request.session['username']
                messages.success(
                    request, f"Account successfully created for {username}! You can login Now")
                return redirect('login')
            else:
                print("not valid form")
                messages.warning(
                    request, f"Invalid username or password. Please Register again")
                return redirect('register')

        else:
            messages.error(request, "Invalid OTP! Please try again")
        return render(request, self.template_name)


class Home(View):
    """
    renders the Register page to the User

    **Context**

    ``form``
        instance of UserRegisterForm class

    **Template:**

    :template:`users/register.html`

    """

    def get(self, request):
        username = request.user
        Quizes = Quiz.objects.all()

        ongoing_quizes = []
        quiz_id_list = []
        taken_quizes = []

        if not (request.user.is_authenticated):
            return render(request, 'users/index.html', {"Quizes": Quizes})

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

        return render(request, 'users/index.html', {"Quizes": quizes, "ongoing_quizes": ongoings})

@method_decorator(login_required, name='dispatch')
class TakeQuiz(View):
    """
    renders the Register page to the User

    **Context**

    ``form``
        instance of UserRegisterForm class

    **Template:**

    :template:`users/register.html`

    """

    def get(self, request):
        continuing = False
        quiz_id = request.GET['quiz_id']
        question_set = Question.objects.filter(quiz_id=quiz_id)
        question_choice_set = {}
        time_limit = 0
        for i in question_set:
            time_limit += i.time_weightage
            if i.type == "MCQ":
                question_choice_set[i] = MCQ_Question.objects.get(
                    question_id=i.question_id)
            elif i.type == "FIB":
                question_choice_set[i] = 'FIB'

        # check if the user is continuing the quiz

        username = request.user
        user_answers = users_answer.objects.filter(username=username)
        question_ids = Question.objects.filter(quiz_id=quiz_id)
        q_id_list = []

        for i in question_ids:
            q_id_list.append(str(i.question_id))

        for i in user_answers:
            if str(i.question_id.question_id) in q_id_list:
                del question_choice_set[i.question_id]
                continuing = True

        if continuing:
            taken = Taken.objects.get(username=username, quiz_id=quiz_id)
            time_limit = int(taken.time_taken)

        (question, choices) = next(iter(question_choice_set.items()))

        if len(list(question_choice_set)) > 1:
            return render(request, 'users/take_quiz.html', {'quiz_id': quiz_id, 'question': question, 'choices': choices, 'time_limit': time_limit, 'last': 'no'})
        else:
            return render(request, 'users/take_quiz.html', {'quiz_id': quiz_id, 'question': question, 'choices': choices, 'time_limit': time_limit, 'last': 'yes'})


def save_data(request):
    """
    Saves the data to the users_answer Model

    and sends the next question to the page

    via JsonResponse.

    """
    # Get the questions and choice set

    quiz_id = request.POST['quiz_id']
    question_set = Question.objects.filter(quiz_id=quiz_id)
    question_choice_set = {}
    for i in question_set:
        if i.type == "MCQ":
            question_choice_set[i] = MCQ_Question.objects.get(
                question_id=i.question_id)
        elif i.type == "FIB":
            question_choice_set[i] = 'FIB'

    if request.method == "POST":
        # Add the answer to the users_answers model
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST['choice']
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        users_answer.objects.create(
            username=username, question_id=question_instance, answer=answer)

        # Get Attempted Questions
        u_answers = users_answer.objects.filter(username=username)
        q_id_list = []
        for i in u_answers:
            q_id_list.append(str(i.question_id.question_id))

        # Delete Attempted questions from the main set of questions
        question_choice_set_copy = question_choice_set
        for i in list(question_choice_set_copy):
            if str(i.question_id) in q_id_list:
                del question_choice_set[i]

        # get the first Key-value pair
        (question, choices) = next(iter(question_choice_set.items()))

        #convert the model to Dictionary
        question_obj = model_to_dict(question)
        question_obj['question_id'] = question.question_id

        # check if the question is the last question
        if len(list(question_choice_set)) > 1:
            if str(question.type) == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices': choices_obj, 'last': 'no'})
            else:
                return JsonResponse({'question': question_obj, 'choices': '__none', 'last': 'no'})

        else:
            if str(question.type) == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices': choices_obj, 'last': 'yes'})
            else:
                return JsonResponse({'question': question_obj, 'choices': '__none', 'last': 'yes'})


def save_and_cont_later(request):
    """
    Saves the state so that user can login 

    later and continue with the quiz.

    """

    if request.method == "POST":

        # Getting post data
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST['choice']
        time_rem = int(request.POST['time_remaining'])
        quiz_id = request.POST['quiz_id']
        last = request.POST.get('last', 'no')

        # Add the answer to the users_answer model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        users_answer.objects.create(
            username=username, question_id=question_instance, answer=answer)

        quiz_id_ins = Quiz.objects.get(quiz_id=quiz_id)

        # check if the question is the last question of the quiz.
        # If it is then submit the quiz
        if last == 'yes':
            marks_weightage = []
            u_answer = []
            correct_answer = []
            question_ids = Question.objects.filter(quiz_id=quiz_id)

            for i in question_ids:
                u_a = users_answer.objects.get(
                    username=username, question_id=i.question_id)
                u_answer.append(u_a.answer)
                marks_weightage.append(i.marks_weightage)
                if i.type == "MCQ":
                    correct_answer.append(MCQ_Question.objects.get(
                        question_id=i.question_id).answer)
                else:
                    correct_answer.append(FIB_Question.objects.get(
                        question_id=i.question_id).answer)

            marks_obt = 0
            for i in range(len(u_answer)):
                if u_answer[i] == correct_answer[i]:
                    marks_obt += marks_weightage[i]

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins, submitted=False).update(
                        submitted=True, marks_obtained=marks_obt, time_taken=time_rem)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=True, marks_obtained=marks_obt, time_taken=time_rem)
        else:

            # check if the user has already saved this quiz before or not
            try:
                if Taken.objects.get(username=username, quiz_id=quiz_id_ins, submitted=False):
                    Taken.objects.filter(username=username, quiz_id=quiz_id_ins).update(
                        time_taken=time_rem)
            except:
                Taken.objects.create(username=username, quiz_id=quiz_id_ins,
                                     submitted=False, marks_obtained=0, time_taken=time_rem)

        return render(request, 'users/logout.html')


@method_decorator(login_required, name='dispatch')
class Results(View):
    """
    Shows the result of the quiz after the

    user has submitted the quiz.

    **Context**

    'marks_obtained': The Marks obtained by the user,
    'total_marks': the Total marks of the quiz,
    'percentage': Percentage of the user,
    'questions': QuerySet of the question objects present in the quiz,
    'users_answer': The answer user has given,
    'correct_answer': The correct answer of the question
    'time_taken': the time taken by the user

    **Template:**

    :template:'users/results.html'

    """
    

    template_name = 'users/results.html'

 
    def post(self, request):
        marks_weightage = []
        u_answer = []
        correct_answer = []

        quiz_id = request.POST.get('quiz_id')
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST['btnradio']
        time_taken = request.POST['time_remaining_input']

        # add the last question to the users_answer Model
        question_instance = Question.objects.filter(
            question_id=question_id).get()
        users_answer.objects.create(
            username=username, question_id=question_instance, answer=answer)
        question_ids = Question.objects.filter(quiz_id=quiz_id)

        # Fetch the correct answers answer the user has given
        for i in question_ids:
            u_a = users_answer.objects.get(
                username=username, question_id=i.question_id)
            u_answer.append(u_a.answer)
            marks_weightage.append(i.marks_weightage)
            if i.type == "MCQ":
                correct_answer.append(MCQ_Question.objects.get(
                    question_id=i.question_id).answer)
            else:
                correct_answer.append(FIB_Question.objects.get(
                    question_id=i.question_id).answer)

        # calculate marks obtained and the percentage
        marks_obt = 0
        for i in range(len(u_answer)):
            if u_answer[i] == correct_answer[i]:
                marks_obt += marks_weightage[i]

        total_marks = sum(marks_weightage)
        perct = ((marks_obt/total_marks) * 100)

        context = {
            'marks_obtained': marks_obt,
            'total_marks': total_marks,
            'percentage': perct,
            'questions': question_ids,
            'users_answer': u_answer,
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

        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class Profile(View):
    """
    Shows the quizes submitted by the user

    **Context**

    'marks_obtained': The Marks obtained by the user,
    'total_marks': the Total marks of the quiz,
    'percentage': Percentage of the user,
    'questions': QuerySet of the question objects present in the quiz,
    'users_answer': The answer user has given,
    'correct_answer': The correct answer of the question

    **Template:**

    :template:'users/results.html'

    **Template:**

    :template: 'users/results.html'

    """


    template_name = 'users/results.html'

    def get(self, request):
        username = request.user
        taken = Taken.objects.filter(username=username, submitted=True)
        quizes = []
        for i in taken:
            quizes.append(i.quiz_id)

        context = {
            'taken': taken,
            'quizes': quizes
        }

        return render(request, 'users/profile.html', context)

    def post(self, request):
        # shows the details of the quiz submitted by
        # the user in the results template

        marks_weightage = []
        u_answer = []
        correct_answer = []

        quiz_id = request.POST['quiz_id']
        username = request.user
        question_ids = Question.objects.filter(quiz_id=quiz_id)

        for i in question_ids:
            u_a = users_answer.objects.get(
                username=username, question_id=i.question_id)
            u_answer.append(u_a.answer)
            marks_weightage.append(i.marks_weightage)
            if i.type == "MCQ":
                correct_answer.append(MCQ_Question.objects.get(
                    question_id=i.question_id).answer)
            else:
                correct_answer.append(FIB_Question.objects.get(
                    question_id=i.question_id).answer)

        marks_obt = 0
        for i in range(len(u_answer)):
            if u_answer[i] == correct_answer[i]:
                marks_obt += marks_weightage[i]

        total_marks = sum(marks_weightage)
        perct = ((marks_obt/total_marks) * 100)

        context = {
            'marks_obtained': marks_obt,
            'total_marks': total_marks,
            'percentage': perct,
            'questions': question_ids,
            'users_answer': u_answer,
            'correct_answer': correct_answer,
        }

        return render(request, self.template_name, context)

import json
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, JsonResponse
from users.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.views import View
from .models import *
from json import dumps


class Register(View):
    
    def get(self, request):
        form = UserRegisterForm()
        return render(request,'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            request.session['email'] = email
            request.session['username'] = username
            return redirect('otp_verification')
        return render(request,'users/register.html', {'form': form})


class OtpVerification(View):
    
    def get(self, request):
        sent = False
        try:
            email = request.session['email']
        except:
            return redirect('register')
        if sent==False:
            otp = random.randint(11111, 99999)
            request.session['otp'] = otp
            send_mail('OTP Verification', f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
            messages.success(request, f"OTP Successfully sent to {email}. Please check your email!")
            sent = True
        else:
            messages.warning(request, f'Already sent email with OTP')
        
        return render(request, 'users/otpverification.html')
        
    def post(self, request):
        entered_otp = request.POST["otp"]
        otp = request.session['otp']
        if int(entered_otp) == int(otp):
            form_data = request.session['form_data']

            form = UserCreationForm(form_data)
            if form.is_valid():
                print("Valid Form")
                User.objects.create(username=form_data['username'], password=form_data['password1'], email=form_data['email'])
                username = request.session['username']
                messages.success(request, f"Account successfully created for {username}! You can login Now")
                return redirect('login') 
            else:
                print("not valid form")
                messages.warning(request, f"Invalid username or password. Please Register again")
                return redirect('register') 
            
        else:
            messages.error(request, "Invalid OTP! Please try again")
        return render(request, 'users/otpverification.html')


class Home(View):

    def get(self, request):
        Quizes = Quiz.objects.all()
        return render(request, 'users/index.html', {"Quizes": Quizes})
    
    def post(self, request):
        quiz_id = request.POST['quiz_id']
        
    def check_if_login(self, request):
        print("inside Login")


class TakeQuiz(View):
    
    def get(self, request):
        if (not request.session.get('quiz_id')):
            request.session['quiz_id'] = request.GET['quiz_id']
        quiz_id = request.session['quiz_id']
        question_set = Question.objects.filter(quiz_id=quiz_id)
        question_choice_set = {}
        time_limit = 0
        for i in question_set:
            time_limit += i.time_weightage
            if i.type=="MCQ":
                question_choice_set[i] = MCQ_Question.objects.get(question_id=i.question_id)
            elif i.type=="FIB":
                question_choice_set[i] = 'FIB'
            
        #return JsonResponse({'status': 'save'})
        #return render(request, 'users/take_quiz.html', {'quiz_id':quiz_id, 'question':question, 'choices':choices})
        
        (question, choices) = next(iter(question_choice_set.items()))

        return render(request, 'users/take_quiz.html', {'quiz_id':quiz_id, 'question': question, 'choices':choices , 'time_limit':time_limit})

    
def save_data(request):
    if (not request.session.get('quiz_id')):
        request.session['quiz_id'] = request.GET['quiz_id']
    quiz_id = request.session['quiz_id']
    question_set = Question.objects.filter(quiz_id=quiz_id)
    question_choice_set = {}
    for i in question_set:
        if i.type=="MCQ":
            question_choice_set[i] = MCQ_Question.objects.get(question_id=i.question_id)
        elif i.type=="FIB":
            question_choice_set[i] = 'FIB'

    if request.method=="POST":
        username = request.user
        question_id = request.POST['question_id']
        answer = request.POST['choice']
        question_instance = Question.objects.filter(question_id=question_id).get()
        users_answer.objects.create(username=username, question_id=question_instance, answer=answer)

        u_answers = users_answer.objects.filter(username=username)
        q_id_list = []
        for i in u_answers:
            q_id_list.append(str(i.question_id.question_id))

        print('Q_id_list: ', q_id_list)

        question_choice_set_copy = question_choice_set
        for i in list(question_choice_set_copy):
            if str(i.question_id) in q_id_list:
                del question_choice_set[i]

        (question, choices) = next(iter(question_choice_set.items()))
            
        question_obj = model_to_dict(question)
        question_obj['question_id'] = question.question_id

        if len(list(question_choice_set)) > 1:
            if question.type == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices':choices_obj, 'last':False})
            else:
                return JsonResponse({'question': question_obj, 'last':False})

        else:
            if question.type == 'MCQ':
                choices_obj = model_to_dict(choices)
                return JsonResponse({'question': question_obj, 'choices':choices_obj, 'last':True})
            else:
                return JsonResponse({'question': question_obj, 'last':True})
            

def results(request):
    if request.method=='POST':
        quiz_id = request.POST.get('quiz_id')
        return render(request, 'results.html')
        # push to Taken table

        # when the user takes remaining quiz
        # try:
        #     attempted_questions = users_answer.objects.filter(username=username)

        #     for i in question_choice_set:
        #         if i.question_id in attempted_questions:
        #             del(question_choice_set[i])

        #     print(question_choice_set)
        #     print(attempted_questions.question_id)
            
        #     print('inside try ajax get')
        #     (question, choices) = next(iter((question_choice_set.items())))

        #     print(question)
        #     print(choices)

        #     return JsonResponse( {'question': question, 'choices':choices})
        #     #return render(request, 'users/take_quiz.html', {'quiz_id':quiz_id, 'question': question, 'choices':choices})
                
        # except:
        #     print('inside except ajax get')
        #     (question, choices) = next(iter((question_choice_set.items())))

        




# def otpverification(request):
#     sent = False
    
#     try:
#         email = request.session['email']
#     except:
#         return redirect('register')

#     if request.method=="POST":
#         entered_otp = request.POST["otp"]
#         otp = request.session['otp']
#         if int(entered_otp) == int(otp):
#             username = request.session['username']
#             messages.success(request, f"Account successfully created for {username}! You can login Now")
#             return redirect('login') 
#         else:
#             messages.error(request, "Invalid OTP! Please try again")
    
#     else:
#         if sent==False:
#             otp = random.randint(11111, 99999)
#             request.session['otp'] = otp
#             send_mail('OTP Verification', f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
#             messages.success(request, f"OTP Successfully sent to {email}. Please check your email!")
#             sent = True
#         else:
#             messages.warning(request, f'Already sent email with OTP')

#     return render(request, 'users/otpverification.html')



class Profile(View):
    @login_required
    def get(self, request):
        return render(request, 'users/profile.html')

# @login_required
# def profile(request):
#     return render(request, 'users/profile.html')
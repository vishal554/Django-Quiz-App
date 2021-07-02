from django.contrib.auth.forms import UserCreationForm
from users.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.views import View
from .models import *


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
        quiz_id = request.GET['quiz_id']
        question_set = Question.objects.filter(quiz_id=quiz_id)
        question_choice_set = {}
        time_limit = 0
        for i in question_set:
            time_limit += i.time_weightage
            if i.type=="MCQ":
                question_choice_set[i] = MCQ_Question.objects.get(question_id=i.question_id)
            elif i.type=="FIB":
                question_choice_set[i] = 'FIB'
        
        print(time_limit)
        
        return render(request, 'users/take_quiz.html', {'quiz_id':quiz_id, 'question_choice_set':question_choice_set, 'time_limit':time_limit})

    def post(self, request):
        quiz_id = request.POST['quiz_id']
        question_set = Question.objects.filter(quiz_id=quiz_id)
        question_choice_set = {}
        for i in question_set:
            if i.type=="MCQ":
                question_choice_set[i] = MCQ_Question.objects.get(question_id=i.question_id)
            elif i.type=="FIB":
                question_choice_set[i] = FIB_Question.objects.get(question_id=i.question_id)
        print(len(question_choice_set))
        user_answers = []
        correct_answers = []
        for (ques,mcq),counter in zip(question_choice_set.items(), range(1, len(question_choice_set)+1)):
            if ques.type == "MCQ":
                user_answers.append(request.POST[f'btnradio{counter}'])
                correct_answers.append(mcq.answer)
            else:
                user_answers.append(request.POST[f'fib_answer{counter}'])
                correct_answers.append(mcq.answer)
        
        print(user_answers)
        print(correct_answers)
        
        return render(request, 'users/profile.html')




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
from django.contrib.auth import forms
from django.http import request
from users.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random
from django.views import View
# Create your views here.



# def register(request):
#     if request.method == "POST":
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get("email")
#             username = form.cleaned_data.get("username")
#             request.session['email'] = email
#             request.session['username'] = username
#             return redirect('otp_verification')
#     else:
#         form = UserRegisterForm()

#     return render(request,'users/register.html', {'form': form})


class Register(View):
    
    def get(self, request):
        form = UserRegisterForm()
        return render(request,'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            request.session['email'] = email
            request.session['username'] = username
            return redirect('otp_verification')

        return render(request,'users/register.html', {'form': form})



class Home(View):
    def get(self, request):
        return render(request, 'users/index.html')


# def home(request):
#     return render(request, 'users/index.html')



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
            #form = request.session['form']
            username = request.session['username']
            messages.success(request, f"Account successfully created for {username}! You can login Now")
            return redirect('login') 
        else:

            messages.error(request, "Invalid OTP! Please try again")

        return render(request, 'users/otpverification.html')


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
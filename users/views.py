import pyotp
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from users.forms import UserRegisterForm
from .models import *


class RegisterView(View):
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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print('valid form')
            request.session['form_data'] = form.cleaned_data
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            request.session['email'] = email
            request.session['username'] = username
            return redirect('otp_verification')
        return render(request, self.template_name, {'form_errors': form.errors})


class OtpVerificationView(View):
    """
    renders the OTP Verification page to the User

    **Template:**

    :template:`users/otpverification.html`

    """
    template_name = 'users/otpverification.html'

    def get(self, request):
        try:
            email = request.session['email']
            otp = request.session.get('otp', '')
        except:
            return redirect('register')
        if otp == '':
            base32 = pyotp.random_base32()
            totp = pyotp.TOTP(base32)
            otp = totp.now()
            request.session['otp'] = otp
            send_mail('OTP Verification',
                      f'Your OTP is: {otp}', 'vishalpanchal338@gmail.com', [email], fail_silently=False)
            messages.success(
                request, f"OTP Successfully sent to {email}. Please check your email!")
        else:
            messages.warning(
                request, f'Already sent email with OTP! please check your email')

        return render(request, self.template_name)

    def post(self, request):
        # check the entered OTP and redirect to respective page
        # depending on whether OTP is correct or not
        entered_otp = request.POST.get("otp", '0')
        try:
            otp = request.session['otp']
        except:
            return redirect('register')

        if int(entered_otp) == int(otp):
            form_data = request.session['form_data']
            form = UserCreationForm(form_data)
            request.session.delete('otp')
            request.session.delete('email')
            request.session.delete('form_data')
            if form.is_valid():
                password = make_password(form_data['password1'])
                User.objects.create(
                    username=form_data['username'], password=password, email=form_data['email'])
                username = request.session['username']

                messages.success(
                    request, f"Account successfully created for {username}! You can login Now")
                return redirect('login')
            else:

                messages.warning(
                    request, f"Invalid username or password. Please Register again")
                return redirect('register')
        else:
            messages.error(request, "Invalid OTP! Please try again")
        return render(request, self.template_name)


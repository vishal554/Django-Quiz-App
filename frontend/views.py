from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name = "frontend/index.html"
class RegisterView(TemplateView):
    template_name = "frontend/register.html"
class LoginView(TemplateView):
    template_name = "frontend/login.html"
class OtpVerificationView(TemplateView):
    template_name = "frontend/otpverification.html"
class LogoutView(TemplateView):
    template_name = "frontend/logout.html"
class TakeQuizView(TemplateView):
    template_name = "frontend/take_quiz.html"
class ProfileView(TemplateView):
    template_name = "frontend/profile.html"
class ResultsView(TemplateView):
    template_name = "frontend/results.html"
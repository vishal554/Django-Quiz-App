
from django.urls import path, include
from django.views.generic.base import TemplateView
from users import views
from django.contrib.auth import login, views as auth_views

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('home/', views.Home.as_view(), name="home"),
    path('otpVerification/', views.OtpVerification.as_view(), name="otp_verification"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('take_quiz/', views.TakeQuiz.as_view(), name="take_quiz")
]

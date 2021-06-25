
from django.urls import path, include
from django.views.generic.base import TemplateView
from users import views
from django.contrib.auth import login, views as auth_views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('home/', views.home, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]

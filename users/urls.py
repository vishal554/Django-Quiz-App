
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from users import views
from django.contrib.auth import login, views as auth_views

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('profile/', views.Profile.as_view(), name="profile"),
    path('home/', views.Home.as_view(), name="home"),
    path('otpVerification/', views.OtpVerification.as_view(), name="otp_verification"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
    path('take_quiz/', views.TakeQuiz.as_view(), name="take_quiz"),
    path('save_data/', views.save_data, name="save_data"),
    path('results/', views.Results.as_view(), name="results"),
    path('save_and_cont_later/', views.save_and_cont_later, name="save_and_cont_later")
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

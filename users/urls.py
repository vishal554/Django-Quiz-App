
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.Register.as_view(), name="register"),
    path('otpVerification/', views.OtpVerification.as_view(), name="otp_verification"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

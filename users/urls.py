
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from django.contrib.auth import views as auth_views
from users.views import(
    RegisterView,
    OtpVerificationView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('otpVerification/', OtpVerificationView.as_view(), name="otp_verification"),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

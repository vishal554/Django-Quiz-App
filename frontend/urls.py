
from django.urls.conf import path
from frontend.views import (
    HomeView,
    RegisterView,
    OtpVerificationView,
    LoginView,
    LogoutView,
    ResultsView,
    ProfileView,
    TakeQuizView
)

urlpatterns = [
    path("home", HomeView.as_view(), name="frontend_home"),
    path("register", RegisterView.as_view(), name="frontend_register"),
    path("login", LoginView.as_view(), name="frontend_login"),
    path("logout", LogoutView.as_view(), name="frontend_logout"),
    path("otpverification", OtpVerificationView.as_view(), name="frontend_otpverification"),
    path("takequiz", TakeQuizView.as_view(), name="frontend_take_quiz"),
    path("results", ResultsView.as_view(), name="frontend_results"),
    path("profile", ProfileView.as_view(), name="frontend_profile"),

]
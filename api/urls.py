from django.conf import settings
from django.urls.conf import path
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from api.views import (
    Home,
    Register,
    OtpVerification,
    Profile,
    Results,
    TakeQuiz
)

urlpatterns = [
    path('home/', Home.as_view(), name='apihome'),
    path('register/', Register.as_view(), name='apiregister'),
    path('otpverification/', OtpVerification.as_view(), name='apiotpverification'),
    path('login/', obtain_auth_token, name='apilogin'),
    path('profile/', Profile.as_view(), name='apiprofile'),
    path('results/', Results.as_view(), name='apiresults'),
    path('takequiz/', TakeQuiz.as_view(), name='apitakequiz'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
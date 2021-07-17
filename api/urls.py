from django.conf import settings
from django.urls.conf import path
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from api.views import (
    HomeView,
    RegisterView,
    OtpVerificationView,
    ProfileView,
    ResultsView,
    SaveView,
    SubmitView,
    TakeQuizView
)

urlpatterns = [
    path('home/', HomeView.as_view(), name='apihome'),
    path('register/', RegisterView.as_view(), name='apiregister'),
    path('otpverification/', OtpVerificationView.as_view(), name='apiotpverification'),
    path('login/', obtain_auth_token, name='apilogin'),
    path('profile/', ProfileView.as_view(), name='apiprofile'),
    path('results/', ResultsView.as_view(), name='apiresults'),
    path('takequiz/', TakeQuizView.as_view(), name='apitakequiz'),
    path('save/', SaveView.as_view(), name='apisave'),
    path('submit/', SubmitView.as_view(), name='apisubmit'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
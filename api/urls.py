from django.conf import settings
from django.urls.conf import path
from api.views import *
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('home/', home, name='home'),
    path('register/', register, name='register'),
    path('otpverification/', otpverification, name='otpverification'),
    path('login/', obtain_auth_token, name='login'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
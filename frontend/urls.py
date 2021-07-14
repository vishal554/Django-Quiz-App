from django.conf import settings
from django.urls.conf import path
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from frontend.views import IndexPage

urlpatterns = [
    path("", IndexPage.as_view(), name="index")
]
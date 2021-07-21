from django.urls.conf import path
from django.conf import settings
from django.conf.urls.static import static
from testing.views import *
urlpatterns = [
    path("detail", company_detail, name="company_detail"),
    path("login", company_login, name="company_login"),
    path("signup", company_signup, name="company_signup"),
    path("people", company_people, name="company_people"),
    path("settings", company_settings, name="company_settings"),
    path("task", company_task, name="company_task"),
    path("task_detail", company_task_detail, name="company_task_detail"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
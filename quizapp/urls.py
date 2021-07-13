from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from quizapp.views import (
    ProfileView,
    HomeView,
    TakeQuizView,
    save_and_cont_later,
    save_data,
    ResultsView
)

urlpatterns = [
    
    path('profile/', ProfileView.as_view(), name="profile"),
    path('home/', HomeView.as_view(), name="home"),
    path('take_quiz/', TakeQuizView.as_view(), name="take_quiz"),
    path('save_data/', save_data, name="save_data"),
    path('results/', ResultsView.as_view(), name="results"),
    path('save_and_cont_later/', save_and_cont_later, name="save_and_cont_later")
    
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

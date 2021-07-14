from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class IndexPage(TemplateView):
    template_name = "frontend/index.html"
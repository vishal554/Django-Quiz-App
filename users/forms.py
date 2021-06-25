from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
    
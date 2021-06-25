from users.forms import UserRegisterForm
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account successfully created for {username}! You can login Now")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request,'users/register.html', {'form': form})

def home(request):
    return render(request, 'index.html')


@login_required
def profile(request):
    return render(request, 'users/profile.html')
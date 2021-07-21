from django.shortcuts import render

# Create your views here.

def company_detail(request):
    return render(request, 'testing/company-detail.html')

def company_login(request):
    return render(request, 'testing/company-login.html')

def company_signup(request):
    return render(request, 'testing/company-signup.html')

def company_people(request):
    return render(request, 'testing/company-people.html')

def company_settings(request):
    return render(request, 'testing/company-settings.html')

def company_task(request):
    return render(request, 'testing/company-task.html')

def company_task_detail(request):
    return render(request, 'testing/company-task-detail.html')

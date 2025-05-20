from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect(f"{reverse('login')}?next=/booking/")
        else:
            return render(request, 'registration/register.html',
                          {'error': 'Username already exists'})
    return render(request, 'registration/register.html')

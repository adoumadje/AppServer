from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def home(request):
   return render(request, 'users/home.html')

@login_required
def private_page(request):
   return render(request, 'users/private.html')

def register(request):
   if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       if not User.objects.filter(username=username).exists():
           User.objects.create_user(username=username, password=password)
           return redirect('login')
       else:
           return render(request, 'users/register.html', {'error': 'Username already exists'})
   return render(request, 'users/register.html')

def login_view(request):
   if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']
       user = authenticate(request, username=username, password=password)
       if user is not None:
           login(request, user)
           return redirect('home')
       else:
           return render(request, 'users/login.html', {'error': 'Invalid credentials'})
   return render(request, 'users/login.html')

def logout_view(request):
   logout(request)
   return redirect('home')
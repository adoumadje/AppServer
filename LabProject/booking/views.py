from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Color, Brand, Features


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

def add_new_car(request):
    colors = Color.objects.all()
    brands = Brand.objects.all()
    features = Features.objects.all()

    context = {
        'colors': colors,
        'brands': brands,
        'features': features,
    }
    if request.method == 'POST':
        pass

    return render(request, 'forms/add_new_car.html', context=context)

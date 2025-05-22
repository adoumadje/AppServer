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

    error = None

    context = {
        'colors': colors,
        'brands': brands,
        'features': features,
        'error': error
    }
    if request.method == 'POST':
        brand_id = request.POST['brand']
        brand = Brand.get_object_or_404(Brand, pk=brand_id)
        color_id = request.POST['color']
        color = Color.get_object_or_404(Color, pk=color_id)
        model = request.POST['model']
        price_per_day = request.POST['price_per_day']
        num_of_seats = request.POST['num_of_seats']

        image = request.FILE['image']
        if(image.size > 2 * 1024 * 1024):
            return render(request, 'forms/add_new_car.html', context=context)
        # File type validation (only JPG and PNG)
        allowed_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_types:
            return render(request, 'forms/add_new_car.html', context=context)



    return render(request, 'forms/add_new_car.html', context=context)

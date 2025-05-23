from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Color, Brand, Features, Car


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

@login_required
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
        owner = request.user
        brand_id = request.POST['brand']
        brand = get_object_or_404(Brand, pk=brand_id)
        color_id = request.POST['color']
        color = get_object_or_404(Color, pk=color_id)
        model = request.POST['model']
        price_per_day = request.POST['price_per_day']
        num_of_seats = request.POST['num_of_seats']

        image = request.FILES['car_image']
        if(image.size > 2 * 1024 * 1024):
            return render(request, 'forms/add_new_car.html', context=context)
        # File type validation (only JPG and PNG)
        allowed_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_types:
            return render(request, 'forms/add_new_car.html', context=context)

        is_available = request.POST['is_available'] == 'on'

        features_ids = request.POST['features']

        car = Car.objects.create(owner=owner,brand=brand, color=color, model=model, price_per_day=price_per_day,
                                num_of_seats=num_of_seats, image=image, is_available=is_available)
        car.features.set(features_ids)
        return redirect('cars')

    return render(request, 'forms/add_new_car.html', context=context)


class CarListView(generic.ListView):
    model = Car

class CarDetailView(generic.DetailView):
    model = Car

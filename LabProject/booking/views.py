from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from datetime import date, datetime

from .models import Color, Brand, Features, Car, Booking, SupportTicket


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
            return render(request, 'forms/car_form.html', context=context)
        # File type validation (only JPG and PNG)
        allowed_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_types:
            return render(request, 'forms/car_form.html', context=context)

        is_available = request.POST['is_available'] == 'on'

        features_ids = request.POST['features']

        car = Car.objects.create(owner=owner,brand=brand, color=color, model=model, price_per_day=price_per_day,
                                num_of_seats=num_of_seats, image=image, is_available=is_available)
        car.features.set(features_ids)
        return redirect('cars')

    return render(request, 'forms/car_form.html', context=context)


class CarListView(generic.ListView):
    model = Car

    def get_queryset(self):
        return Car.objects.filter(is_available=True)

class MyCarListView(generic.ListView):
    model = Car
    template_name = 'booking/my_cars_list.html'
    context_object_name = 'car_list'
    def get_queryset(self):
        return Car.objects.filter(is_available=True, owner=self.request.user)

@login_required
def edit_my_car(request, pk):
    car = get_object_or_404(Car, pk=pk)
    colors = Color.objects.all()
    brands = Brand.objects.all()
    features = Features.objects.all()

    error = None

    context = {
        'car': car,
        'colors': colors,
        'brands': brands,
        'features': features,
        'error': error
    }
    if request.method == 'POST':
        car.owner = request.user
        brand_id = request.POST['brand']
        car.brand = get_object_or_404(Brand, pk=brand_id)
        color_id = request.POST['color']
        car.color = get_object_or_404(Color, pk=color_id)
        car.modelmodel = request.POST['model']
        car.price_per_day = request.POST['price_per_day']
        car.num_of_seats = request.POST['num_of_seats']

        if request.FILES.get('car_image'):
            image = request.FILES['car_image']
            if (image.size > 2 * 1024 * 1024):
                return render(request, 'forms/car_form.html', context=context)
            # File type validation (only JPG and PNG)
            allowed_types = ['image/jpeg', 'image/png']
            if image.content_type not in allowed_types:
                return render(request, 'forms/car_form.html', context=context)
            car.image = image

        car.is_available = request.POST['is_available'] == 'on'

        car.save()

        features_ids = request.POST['features']
        car.features.set(features_ids)
        return redirect(car.get_absolute_url())

    return render(request, 'forms/car_form.html', context=context)

class CarDetailView(generic.DetailView):
    model = Car

@login_required
def book_car(request, pk):
    car = get_object_or_404(Car, pk=pk)

    error = None

    context = {
        'car': car,
        'error': error
    }

    if request.method == 'POST':
        user = request.user
        start_date_str = request.POST['start_date']
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date_str = request.POST['end_date']
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        status = 'Pending'

        if start_date < date.today():
            context['error'] = 'start date can be in the past'
            return render(request, 'booking/book_car.html', context=context)
        if end_date < start_date:
            context['error'] = "end date can't be before start date"
            return render(request, 'booking/book_car.html', context=context)

        car.is_available = False
        car.save()

        Booking.objects.create(user=user, car=car, start_date=start_date, end_date=end_date,
                               status=status)
        return redirect('my_bookings')


    return render(request, 'booking/book_car.html', context=context)


class BookingListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'booking/my_bookings.html'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class MyCarsBookingRequestsListView(LoginRequiredMixin, generic.ListView):
    model = Booking
    template_name = 'booking/my_cars_booking_requests.html'
    context_object_name = 'booking_list'

    def get_queryset(self):
        return Booking.objects.filter(car__owner=self.request.user, status='Pending')

@login_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    car = booking.car
    car.is_available = True
    car.save()
    booking.status = 'Confirmed'
    booking.save()
    return redirect('my_cars_booking_requests')

@login_required
def reject_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    car = booking.car
    car.is_available = True
    car.save()
    booking.status = 'Cancelled'
    booking.save()
    return redirect('my_cars_booking_requests')

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    car = booking.car
    car.is_available = True
    car.save()
    booking.status = 'Cancelled'
    booking.save()
    return redirect('my_bookings')

@login_required
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        car = booking.car
        car.is_available = True
        car.save()
        booking.delete()
        return redirect('my_bookings')
    return render(request, 'booking/delete_booking.html', {'booking': booking})

@login_required
def open_support_ticket(request):
    user = request.user
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        status = 'Open'
        SupportTicket.objects.create(user=user, subject=subject, message=message, status=status)
        return redirect('my_support_tickets')
    return render(request, 'forms/open_support_ticket.html')

class SupportTicketListView(LoginRequiredMixin, generic.ListView):
    model = SupportTicket
    template_name = 'booking/my_support_tickets.html'

def search_cars(request):
    results = []
    if request.method == 'POST':
        query = request.POST['query']
        results = Car.objects.filter(
            Q(model__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(color__name__icontains=query) |
            Q(owner__username__icontains=query)
        )
    context = {
        'results': results,
    }
    return render(request, 'forms/search_cars.html', context=context)
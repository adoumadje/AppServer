from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')  # many-to-one
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.IntegerField()
    image = models.ImageField(upload_to='car_images/')  # file support
    available = models.BooleanField(default=True)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])


class Feature(models.Model):
    name = models.CharField(max_length=100)

class CarFeature(models.Model):  # many-to-many through model
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[('open', 'Open'), ('closed', 'Closed')])
    created_at = models.DateTimeField(auto_now_add=True)

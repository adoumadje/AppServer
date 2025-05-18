from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Brand(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Features(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Many-To-One
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True) # Many-To-One
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True) # Many-To-One
    model = models.CharField(max_length=100)
    price_per_day=models.DecimalField(max_digits=8, decimal_places=2)
    seats = models.PositiveIntegerField()
    image = models.ImageField(upload_to='car_images/') # File support
    available = models.BooleanField(default=True)
    features = models.ManyToManyField(Features, help_text='Select one or more features for this car')

    def __str__(self):
        return f"{self.brand.name} - {self.model}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return f"Booking by {self.user.username} for {self.car} - {self.status}"


class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('open', 'Open'),
        ('closed', 'Closed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket from {self.user.username} : {self.subject}"

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

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')

class Car(models.Model):
    pass
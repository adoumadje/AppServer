from django.db import models

# Create your models here.

class Category(models.Model):
   name = models.CharField(max_length=100)

   def __str__(self):
       return self.name

class Product(models.Model):
   name = models.CharField(max_length=255)  # A string field with a max length of 255
   weight = models.FloatField()  # A float field
   production_date = models.DateField()  # A date field
   category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1);

   def __str__(self):
       return f"{self.name} - (weight: {self.weight})"  # This makes the product name appear in Django Admin


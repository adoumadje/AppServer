from datetime import date

from django.shortcuts import render, redirect, get_object_or_404

from .models import Product


# Create your views here.

# Read (List)
def product_list(request):
   products = Product.objects.all()  # Fetch all products
   return render(request, 'products/product_list.html', {'products': products})

# Create
def product_create(request):
   if request.method == 'POST':
       name = request.POST.get('name')
       weight = float(request.POST.get('weight'))
       production_date = request.POST.get('production_date')

       if weight <= 0 or production_date >= str(date.today()):
           return render(request, 'products/product_form.html', {'error': 'Invalid data entered.'})

       Product.objects.create(name=name, weight=weight, production_date=production_date)
       return redirect('product_list')
   return render(request, 'products/product_form.html')

# Update
def product_update(request, pk):
   product = get_object_or_404(Product, pk=pk)
   if request.method == 'POST':
       weight = float(request.POST.get('weight'))
       production_date = request.POST.get('production_date')

       if weight <= 0 or production_date >= str(date.today()):
           return render(request, 'products/product_form.html', {'product': product, 'error': 'Invalid data entered.'})

       product.name = request.POST.get('name')
       product.weight = weight
       product.production_date = production_date
       product.save()
       return redirect('product_list')
   return render(request, 'products/product_form.html', {'product': product})

# Delete
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_delete.html', {'product': product})

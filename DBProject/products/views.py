from datetime import date

from django.shortcuts import render, redirect, get_object_or_404

from .models import Product, Category


# Create your views here.

# Read (List)
def product_list(request):
   products = Product.objects.all()  # Fetch all products
   return render(request, 'products/product_list.html', {'products': products})

# Create
def product_create(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        weight = float(request.POST.get('weight'))
        production_date = request.POST.get('production_date')
        category_id = request.POST.get('category')
        category = get_object_or_404(Category, pk=category_id)

        if weight <= 0 or production_date >= str(date.today()):
            return render(request, 'products/product_form.html', {'error': 'Invalid data entered.'})

        Product.objects.create(name=name, weight=weight, production_date=production_date, category=category)
        return redirect('product_list')
    return render(request, 'products/product_form.html', {'categories': categories})


# Update
def product_update(request, pk):
   categories = Category.objects.all()
   product = get_object_or_404(Product, pk=pk)
   if request.method == 'POST':
       weight = float(request.POST.get('weight'))
       production_date = request.POST.get('production_date')
       category_id = request.POST.get('category')
       category = get_object_or_404(Category, pk=category_id)

       if weight <= 0 or production_date >= str(date.today()):
           return render(request, 'products/product_form.html', {'product': product, 'error': 'Invalid data entered.'})

       product.name = request.POST.get('name')
       product.weight = weight
       product.production_date = production_date
       product.category = category
       product.save()
       return redirect('product_list')
   return render(request, 'products/product_form.html', {'product': product, 'categories': categories})

# Delete
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_delete.html', {'product': product})

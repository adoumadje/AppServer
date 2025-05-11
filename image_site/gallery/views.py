from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Photo

# Create your views here.

def upload_photo(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.FILES['image']

        # File size validation (2MB max)
        if image.size > 2 * 1024 * 1024:  # 2MB limit
            return render(request, 'upload.html', {'error': 'File too large. Max size is 2MB.'})

        # File type validation (only JPG and PNG)
        allowed_types = ['image/jpeg', 'image/png']
        if image.content_type not in allowed_types:
            return render(request, 'upload.html', {'error': 'Invalid file type. Only JPG and PNG are allowed.'})

        # Save the photo and show success message
        Photo.objects.create(title=title, image=image)
        messages.success(request, 'Your photo has been uploaded successfully!')
        return redirect('gallery')

    return render(request, 'upload.html')

def gallery_view(request):
    photos = Photo.objects.all()
    return render(request, 'gallery.html', {'photos': photos})

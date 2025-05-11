from django.urls import path
from .views import upload_photo, gallery_view

urlpatterns = [
    path('upload/', upload_photo, name='upload_photo'),
    path('', gallery_view, name='gallery'),
]
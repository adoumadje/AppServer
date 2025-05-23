from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add_new_car/', views.add_new_car, name='add_new_car'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-details')
]
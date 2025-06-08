from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add_new_car/', views.add_new_car, name='add_new_car'),
    path('edit_my_car/<int:pk>', views.edit_my_car, name='edit_my_car'),
    path('my_cars_list/', views.MyCarListView.as_view(), name='my_cars_list'),
    path('cars/', views.CarListView.as_view(), name='cars'),
    path('cars/<int:pk>', views.CarDetailView.as_view(), name='car-details'),
    path('book_car/<int:pk>', views.book_car, name='book_car'),
    path('my_bookings/', views.BookingListView.as_view(), name='my_bookings'),
    path('my_cars_booking_requests/', views.MyCarsBookingRequestsListView.as_view(),
         name='my_cars_booking_requests'),
    path('confirm_booking/<int:pk>', views.confirm_booking, name='confirm_booking'),
    path('reject_booking/<int:pk>', views.reject_booking, name='reject_booking'),
    path('cancel_booking/<int:pk>', views.cancel_booking, name='cancel_booking'),
    path('delete_booking/<int:pk>', views.delete_booking, name='delete_booking'),
    path('open_support_ticket/', views.open_support_ticket, name='open_support_ticket'),
    path('my_support_tickets/', views.SupportTicketListView.as_view(), name='my_support_tickets'),
    path('search', views.search_cars, name='search')
]
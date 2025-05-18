from django.contrib import admin

from .models import Brand, Features, Color, Car, Booking, SupportTicket


# Register your models here.

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    pass

@admin.register(Features)
class FeaturesAdmin(admin.ModelAdmin):
    pass

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    pass
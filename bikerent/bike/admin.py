from django.contrib import admin
from .models import Bike, RentalStation, BikeAtStation, Customer, Rental

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ['name', 'bike_type', 'price_per_hour', 'status', 'created_at']
    list_filter = ['bike_type', 'status', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['status']

@admin.register(RentalStation)
class RentalStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'capacity']
    search_fields = ['name', 'address']

@admin.register(BikeAtStation)
class BikeAtStationAdmin(admin.ModelAdmin):
    list_display = ['bike', 'station', 'arrived_at']
    list_filter = ['station', 'arrived_at']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'phone']

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'bike', 'start_time', 'end_time', 'total_cost', 'status']
    list_filter = ['status', 'start_time']
    search_fields = ['customer__user__first_name', 'customer__user__last_name', 'bike__name']
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Bike, RentalStation, Rental, Customer

def bike_list(request):
    """Список всех велосипедов"""
    bikes = Bike.objects.all()
    bikes_data = []
    for bike in bikes:
        bikes_data.append({
            'id': bike.id,
            'name': bike.name,
            'bike_type': bike.bike_type,
            'price_per_hour': float(bike.price_per_hour),
            'status': bike.status,
        })
    return JsonResponse(bikes_data, safe=False)

def bike_detail(request, bike_id):
    """Детальная информация о велосипеде"""
    bike = get_object_or_404(Bike, id=bike_id)
    bike_data = {
        'id': bike.id,
        'name': bike.name,
        'bike_type': bike.bike_type,
        'description': bike.description,
        'price_per_hour': float(bike.price_per_hour),
        'status': bike.status,
        'created_at': bike.created_at.isoformat(),
    }
    return JsonResponse(bike_data)

def available_bikes(request):
    """Список доступных велосипедов"""
    bikes = Bike.objects.filter(status='available')
    bikes_data = []
    for bike in bikes:
        bikes_data.append({
            'id': bike.id,
            'name': bike.name,
            'bike_type': bike.bike_type,
            'price_per_hour': float(bike.price_per_hour),
        })
    return JsonResponse(bikes_data, safe=False)

def stations_list(request):
    """Список всех станций"""
    stations = RentalStation.objects.all()
    stations_data = []
    for station in stations:
        stations_data.append({
            'id': station.id,
            'name': station.name,
            'address': station.address,
            'capacity': station.capacity,
        })
    return JsonResponse(stations_data, safe=False)

def home(request):
    """Главная страница API"""
    return JsonResponse({
        'message': 'Добро пожаловать в BikeRent API!',
        'endpoints': {
            'all_bikes': '/bike/bikes/',
            'available_bikes': '/bike/available/',
            'bike_detail': '/bike/bikes/<id>/',
            'stations': '/bike/stations/',
        }
    })
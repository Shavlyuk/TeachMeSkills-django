from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/<int:bike_id>/', views.bike_detail, name='bike_detail'),
    path('available/', views.available_bikes, name='available_bikes'),
    path('stations/', views.stations_list, name='stations_list'),
]
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Bike(models.Model):
    BIKE_TYPES = [
        ('mountain', 'Горный'),
        ('road', 'Шоссейный'),
        ('city', 'Городской'),
        ('electric', 'Электрический'),
    ]

    STATUS_CHOICES = [
        ('available', 'Доступен'),
        ('rented', 'Арендован'),
        ('maintenance', 'На обслуживании'),
    ]

    name = models.CharField(max_length=100, verbose_name='Название')
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPES, verbose_name='Тип велосипеда')
    description = models.TextField(verbose_name='Описание', blank=True)
    price_per_hour = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Цена за час',
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеды'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_bike_type_display()})"


class RentalStation(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название станции')
    address = models.CharField(max_length=200, verbose_name='Адрес')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    bikes = models.ManyToManyField(Bike, through='BikeAtStation', verbose_name='Велосипеды')

    class Meta:
        verbose_name = 'Станция аренды'
        verbose_name_plural = 'Станции аренды'

    def __str__(self):
        return self.name


class BikeAtStation(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, verbose_name='Велосипед')
    station = models.ForeignKey(RentalStation, on_delete=models.CASCADE, verbose_name='Станция')
    arrived_at = models.DateTimeField(auto_now_add=True, verbose_name='Прибыл на станцию')

    class Meta:
        verbose_name = 'Велосипед на станции'
        verbose_name_plural = 'Велосипеды на станциях'
        unique_together = ['bike', 'station']


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.TextField(verbose_name='Адрес')
    id_number = models.CharField(max_length=50, verbose_name='Номер удостоверения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Rental(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('completed', 'Завершена'),
        ('cancelled', 'Отменена'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Клиент')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, verbose_name='Велосипед')
    start_station = models.ForeignKey(
        RentalStation,
        on_delete=models.CASCADE,
        related_name='start_rentals',
        verbose_name='Станция начала'
    )
    end_station = models.ForeignKey(
        RentalStation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='end_rentals',
        verbose_name='Станция окончания'
    )
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Время начала')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='Время окончания')
    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Общая стоимость'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'
        ordering = ['-start_time']

    def __str__(self):
        return f"Аренда #{self.id} - {self.customer}"
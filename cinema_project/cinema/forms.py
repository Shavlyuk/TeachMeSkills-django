# cinema/forms.py
from django import forms
from .models import Genre


class SessionFilterForm(forms.Form):
    movie_title = forms.CharField(
        required=False,
        label='Название фильма',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по названию'})
    )

    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        label='Жанр',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date_from = forms.DateField(
        required=False,
        label='С даты',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    date_to = forms.DateField(
        required=False,
        label='По дату',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    price_min = forms.DecimalField(
        required=False,
        label='Цена от',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )

    price_max = forms.DecimalField(
        required=False,
        label='Цена до',
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000'})
    )
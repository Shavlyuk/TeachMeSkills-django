# cinema/views.py
from django.shortcuts import render
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Session
from .forms import SessionFilterForm


def schedule(request):
    sessions = Session.objects.filter(start_time__gte=timezone.now())

    form = SessionFilterForm(request.GET or None)

    if form.is_valid():
        movie_title = form.cleaned_data.get('movie_title')
        genre = form.cleaned_data.get('genre')
        date_from = form.cleaned_data.get('date_from')
        date_to = form.cleaned_data.get('date_to')
        price_min = form.cleaned_data.get('price_min')
        price_max = form.cleaned_data.get('price_max')

        if movie_title:
            sessions = sessions.filter(movie__title__icontains=movie_title)
        if genre:
            sessions = sessions.filter(movie__genres=genre)
        if date_from:
            sessions = sessions.filter(start_time__date__gte=date_from)
        if date_to:
            sessions = sessions.filter(start_time__date__lte=date_to)
        if price_min:
            sessions = sessions.filter(price__gte=price_min)
        if price_max:
            sessions = sessions.filter(price__lte=price_max)

    # Пагинация
    paginator = Paginator(sessions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    filter_params = request.GET.copy()
    if 'page' in filter_params:
        del filter_params['page']
    filter_query_string = filter_params.urlencode()

    context = {
        'page_obj': page_obj,
        'form': form,
        'filter_query_string': filter_query_string
    }

    return render(request, 'cinema/schedule.html', context)

def home(request):
    return render(request, 'cinema/home.html')
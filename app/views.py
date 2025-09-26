import pytz
from datetime import datetime
from typing import Any

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def welcome(
        request: HttpRequest, 
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any]
        ) -> HttpResponse:
    """Return welcome page"""
    return render(request=request, template_name="welcome.html", status=200)



def users_list(
        request: HttpRequest, 
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any]
        ) -> HttpResponse:
    """Show list of users"""
    users: dict[str, Any] = [
        {'full_name': 'Kira Yoshikage', 'age': 33},
        {'full_name': 'Yagami Light', 'age': 23},
        {'full_name': 'Kazuma Sato', 'age': 16},
    ]
    return render(request, 'users.html', {'users': users}, status=200)



def city_time(
        request: HttpRequest, 
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any]
        ) -> HttpResponse:
    cities: dict[str, Any] = {
        'Tokyo': 'Asia/Tokyo',
        'Almaty': 'Asia/Almaty',
        'Bishkek': 'Asia/Bishkek',
        'UTC': 'UTC',
        }
    selected_city=request.GET.get('city')
    current_time = None
    if selected_city in cities:
        time_zone = pytz.timezone(cities[selected_city])
        current_time = datetime.now(time_zone)   
    return render(request, 'city_time.html', 
                  {'cities': cities.keys(),
                   'selected': selected_city, 
                   'current_time': current_time}, 
                   status=200)



def counter(
        request: HttpRequest, 
        *args: tuple[Any, ...], 
        **kwargs: dict[str, Any]
        ) -> HttpResponse:
    return render(request,template_name='counter.html', status=200)


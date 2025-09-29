from datetime import datetime
from zoneinfo import available_timezones, ZoneInfo

from django.shortcuts import render


def welcome_page_vies(request):
    """Returns welcome page of a website."""
    return render(request, template_name="pages/welcome.html")


def users_list_view(request):
    """Returns information about users."""
    users_list = [
        {"first_name": "Alice", "last_name": "Snow", "age": 23},
        {"first_name": "John", "last_name": "Doe", "age": 18},
        {"first_name": "Bob", "last_name": "Miller", "age": 40},
    ]
    context = {
        "users": users_list,
    }

    return render(request, template_name="pages/users.html", context=context)


def city_time_view(request):
    """Returns time for a chosen city."""
    city = request.GET.get("city")
    available_zones = sorted(available_timezones())

    if city:
        city = city.replace("%2F", "/")
        time_now = datetime.now().astimezone(ZoneInfo(city)).strftime("%d-%m-%Y %H:%M:%S")
        print(time_now)
    else:
        time_now = None

    context = {
        "cities": available_zones,
        "current_city": city,
        "time_now": time_now,
    }

    return render(
        request,
        template_name="pages/city_time.html",
        context=context,
    )


def counter_view(request):
    """Returns counter page."""
    return render(request, template_name="pages/counter.html")

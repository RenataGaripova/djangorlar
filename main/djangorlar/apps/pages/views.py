from django.shortcuts import render


def welcome_page_vies(request):
    """Returns welcome page of a website."""
    return render("welcome.html")


def users_list_view(request):
    """Returns information about users."""
    users_list = {
        {"first_name": "Alice", "last_name": "Snow", "age": 23},
        {"first_name": "John", "last_name": "Doe", "age": 18},
        {"first_name": "Bob", "last_name": "Miller", "age": 40},
    }

    context = {
        "users": users_list,
    }

    return render("pages/users.html", context=context)

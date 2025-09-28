from django.urls import path

from . import views

app_name = "pages"


urlpatterns = [
    path('', views.welcome_page_vies, name="welcome_page"),
    path('users/', views.users_list_view, name="users_page"),
]

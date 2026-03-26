from django.urls import path
from .views import greet_function

urlpatterns=[
    path("greet/", greet_function)
]
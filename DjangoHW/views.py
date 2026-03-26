from django.shortcuts import render
from django.http import HttpResponse

def greet_function(request):
    return HttpResponse("<h1>Hello My Friend<h1>")
# Create your views here.

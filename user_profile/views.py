from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return "Hello World!"


def my_profile(request):
    return "Hello World!"


def settings(request):
    return "Hello World!"


def login(request):
    return HttpResponse("Hello World!")

from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'index.html')


def sneakers(request):
    return render(request, 'sneakers.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def contact(request):
    return render(request, 'contact.html')

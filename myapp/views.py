
import email
import re
from django.shortcuts import render
from .models import Contact, User


# Create your views here.


def index(request):
    return render(request, 'index.html')


def sneakers(request):
    return render(request, 'sneakers.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg = "Email already registered."
            return render(request, 'signup.html', {"msg": msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                    cpassword=request.POST['cpassword'],


                )
                msg = "Signup Successfull"
                return render(request, 'login.html', {'msg': msg})
            else:
                msg = "Password doesnot match"
                return render(request, 'signup.html', {'msg': msg})
    else:
        return render(request, 'signup.html')


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            addinfo=request.POST['addinfo'],
        )
        msg = "Request Sent Successfully"
        return render(request, 'contact.html', {'msg': msg})

    else:
        return render(request, 'contact.html')

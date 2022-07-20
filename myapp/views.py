
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
    if request.method == "POST":
        try:
            user = User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
            )
            return render(request, 'index.html')
        except:
            msg = "Email or password incorrect"
            return render(request, 'login.html', {'msg': msg})
    else:
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


def forgot_password(request):
    return render(request, 'forgot_password.html')


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


def verify_otp(request):
    otp = request.POST['otp']
    uotp = request.POST['uotp']
    email = request.POST['email']

    if otp == uotp:
        return render(request, 'new_password.html', {'email': email})

    else:
        msg = "OTP is incorrect. "
        return render(request, 'otp.html', {'email': email, 'otp': otp, 'msg': msg})


def new_passworf(request):
    email = request.POST['email']
    new_password = request.POST['new_password']
    cnew_password = request.POST['cnew_password']

    return render(request, 'login.html')

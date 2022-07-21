from django.shortcuts import redirect, render
from .models import Contact, User
from django.conf import settings
from django.core.mail import send_mail
import random


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
            request.session['email'] = user.email
            request.session['fname'] = user.fname
            return render(request, 'index.html')
        except:
            msg = "Email or password incorrect"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request, 'index.html')
    except:
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
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            otp = random.randint(1000, 9999)
            subject = 'One Time Password'
            message = 'Hi '+user.fname + \
                ', Here Is Your One Time Password :' + str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, 'otp.html', {'otp': otp, 'email': user.email})

        except:
            msg = "Email Not Registered Yet."
            return render(request, 'forgot_password.html', {'msg': msg})

    else:
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


def account_info(request):
    user = User.objects.get(email=request.session['email'])
    if request.method == "POST":
        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.email = request.POST['email']

        return render(request, 'account_info.html', {'user': user})
    else:
        return render(request, 'account_info.html', {'user': user})


def change_password(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        if request.POST['password'] == user.password:
            if request.POST['new_password'] == request.POST['cnew_password']:
                user.password = request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg = "Both Password Doesnot Match"
                return render(request, 'change_password.html', {'msg': msg})
        else:
            msg = "Old Password Doesnot Match"
            return render(request, 'change_password.html', {'msg': msg})
    else:
        return render(request, 'change_password.html')


def new_password(request):
    email = request.POST['email']
    new_password = request.POST['new_password']
    cnew_password = request.POST['cnew_password']

    if new_password == cnew_password:
        user = User.objects.get(email=email)
        user.password = new_password
        user.save()
        msg = "Password Updated Succesfully. You May Login Now"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "Password Didn't Match"
        return render(request, 'new_password.html', {'email': email, 'msg': msg})

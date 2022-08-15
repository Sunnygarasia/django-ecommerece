from django import apps
from django.shortcuts import redirect, render
from .models import Contact, Order, User, Sneaker, Cart
from django.conf import settings
from django.core.mail import send_mail
import random
import stripe
stripe.api_key = settings.SECRET_KEY


# Create your views here.


def index(request):
    return render(request, 'index.html')


def sneakers(request):
    try:
        user = User.objects.get(email=request.session['email'])
        sneakers = Sneaker.objects.filter(user=user)
        if request.method == "POST":
            user.fname = request.POST['fname']
            user.lname = request.POST['lname']
            user.email = request.POST['email']

            return render(request, 'sneakers.html', {'user': user})
        else:

            return render(request, 'sneakers.html', {'sneakers': sneakers})
    except:
        return render(request, 'sneakers.html')


def sneaker_detail(request, pk):
    sneaker = Sneaker.objects.get(pk=pk)
    return render(request, 'sneaker_detail.html', {'sneaker': sneaker})


def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(
                email=request.POST['email'],
                password=request.POST['password']
            )
            request.session['email'] = user.email
            request.session['fname'] = user.fname
            carts = Cart.objects.filter(user=user)
            request.session['cart_count'] = len(carts)
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


def sell_sneaker(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        Sneaker.objects.create(
            user=user,
            sneaker_name=request.POST['sneaker_name'],
            sneaker_size=request.POST['sneaker_size'],
            sneaker_price=request.POST['sneaker_price'],
            sneaker_desc=request.POST['sneaker_desc'],
            sneaker_image=request.FILES['sneaker_image'],

        )
        msg = "Sneaker Added Successfully"
        return render(request, 'sell_sneaker.html', {'msg': msg})

    else:
        return render(request, 'sell_sneaker.html')


def cart(request):

    net_price = 0
    user = User.objects.get(email=request.session['email'])
    carts = Cart.objects.filter(user=user)
    for i in carts:
        for i in carts:
            net_price = net_price+i.total_price
            request.session['cart_count'] = len(carts)
        return render(request, 'cart.html', {'carts': carts, 'net_price': net_price})


def add_to_cart(request, pk):
    sneaker = Sneaker.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    Cart.objects.create(sneaker=sneaker, user=user,
                        sneaker_qty=1,
                        sneaker_price=sneaker.sneaker_price,
                        total_price=sneaker.sneaker_price
                        )
    return redirect('cart')


def remove_from_cart(request, pk):
    sneaker = Sneaker.objects.get(pk=pk)
    user = User.objects.get(email=request.session['email'])
    cart = Cart.objects.get(user=user, sneaker=sneaker)
    cart.delete()
    return redirect('cart')


def change_qty(request):
    pk = int(request.POST['pk'])
    cart = Cart.objects.get(pk=pk)
    sneaker_qty = int(request.POST['sneaker_qty'])
    cart.sneaker_qty = sneaker_qty
    cart.total_price = sneaker_qty*sneaker_price
    cart.save()
    return redirect('cart')


def payment(request):
    net_price = int(request.POST['net_price'])
    return render(request, 'payment.html', {'net_price': net_price, 'key': settings.PUBLISHABLE_KEY})


def success(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        net_price = request.POST['net_price']
        charge = stripe.Charge.create(
            amount=int(net_price),
            currency='usd',
            description='A Payment Gateway',
            source=request.POST['stripeToken']
        )
        carts = Cart.objects.filter(user=user)
        for i in carts:
            i.payment_status = "paid"
            i.save()
        Order.objects.create(
            user=user,
            net_price=net_price,
            stripToken=request.POST['stripeToken']
        )
    return render(request, 'success.html')

import datetime
from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    addinfo = models.TextField()

    def __str__(self):
        return self.name


class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.fname + " - " + self.lname


class Sneaker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sneaker_name = models.CharField(max_length=100)
    sneaker_size = models.CharField(max_length=10)
    sneaker_price = models.PositiveIntegerField()
    sneaker_desc = models.TextField()
    sneaker_image = models.ImageField(upload_to="sneaker_image/")

    def __str__(self):
        return self.user.fname + " - " + self.sneaker_name


class Cart(models.Model):
    sneaker = models.ForeignKey(Sneaker, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.date.today)
    sneaker_qty = models.PositiveIntegerField(default=1)
    sneaker_price = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    payment_status = models.CharField(max_length=100, default="pending")

    def __str__(self):
        return self.user.fname + " - " + self.sneaker.sneaker_name

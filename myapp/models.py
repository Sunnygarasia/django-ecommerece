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
    cpassword = models.CharField(max_length=50)

    def __str__(self):
        return self.fname + " - " + self.lname

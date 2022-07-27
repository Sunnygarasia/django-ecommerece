from django.contrib import admin
from .models import Contact, User, Sneaker, Cart

# Register your models here.
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Sneaker)
admin.site.register(Cart)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sneakers/', views.sneakers, name='sneakers'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('account_info/', views.account_info, name='account_info'),
    path('contact/', views.contact, name='contact'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('change_password/', views.change_password, name='change_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('sell_sneaker/', views.sell_sneaker, name='sell_sneaker'),
    path('sneaker_detail/<int:pk>/',
         views.sneaker_detail, name="sneaker_detail"),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('remove_from_cart/<int:pk>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('change_qty/', views.change_qty, name='change_qty')


]

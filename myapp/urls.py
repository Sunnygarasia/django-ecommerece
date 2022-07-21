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
    path('new_password/', views.new_password, name='new_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),


]

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginnow, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('checkout/<int:package_id>/', views.checkout_now, name='checkout'),
    path('checkout/response/success/', views.checkout_success, name='checkout_success'),
    path('contact/us/', views.message_us, name='contact_us'),
    path('user/', views.my_user, name='user'),
    path('event/data/',views.event_date_filter)
]

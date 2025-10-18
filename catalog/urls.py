# catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL utama untuk daftar mobil: /cars/
    path('', views.car_home, name='car_home'), 
    path('list/', views.car_list, name='car_list'), 
    # URL detail mobil: /cars/1/
    path('<int:car_id>/', views.car_detail, name='car_detail'),
    
    # TAMBAHKAN URL BARU INI
    path('book/<int:car_id>/', views.book_car, name='book_car'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('register/', views.register, name='register'),
]
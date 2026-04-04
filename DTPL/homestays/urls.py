from django.urls import path
from . import views

app_name = 'homestays'

urlpatterns = [
    # Halaman Katalog (Daftar Homestay)
    path('', views.homestay_list, name='list'),
    
    # Halaman Detail Homestay
    path('<slug:slug>/', views.homestay_detail, name='detail'),
    
    # Proses Kirim Booking (POST)
    path('<slug:slug>/book/', views.homestay_booking_create, name='booking_create'),
]
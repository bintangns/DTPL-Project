from django.urls import path
from . import views

app_name = 'homestays_admin'

urlpatterns = [
    path('', views.admin_homestay_list, name='list'),
    path('bookings/', views.admin_homestay_booking_list, name='booking_list'),
]

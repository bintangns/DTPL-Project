from django.urls import path
from . import views

app_name = 'guide'

urlpatterns = [
    # Public: booking paket wisata
    path('<slug:dest_slug>/<slug:pkg_slug>/book/', views.package_booking_create, name='booking_create'),
    path('booking-success/<int:pk>/', views.booking_success, name='booking_success'),
]

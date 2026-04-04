from django.urls import path
from . import views

app_name = 'homestays_admin'

urlpatterns = [
    # CRUD Homestay
    path('', views.admin_homestay_list, name='list'),
    path('create/', views.admin_homestay_create, name='create'),
    path('update/<int:pk>/', views.admin_homestay_update, name='update'),
    path('delete/<int:pk>/', views.admin_homestay_delete, name='delete'),
    
    # Manajemen Booking/Pemesanan
    path('bookings/', views.admin_homestay_booking_list, name='booking_list'),
    path('bookings/status/<int:pk>/', views.admin_booking_update_status, name='booking_update'),
]
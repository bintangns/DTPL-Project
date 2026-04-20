from django.urls import path
from . import views

app_name = 'guide_admin'

urlpatterns = [
    # CRUD Pemandu Wisata
    path('guides/', views.admin_guide_list, name='guide_list'),
    path('guides/create/', views.admin_guide_create, name='guide_create'),
    path('guides/<int:pk>/edit/', views.admin_guide_edit, name='guide_edit'),
    path('guides/<int:pk>/delete/', views.admin_guide_delete, name='guide_delete'),

    # CRUD Paket Wisata
    path('packages/', views.admin_package_list, name='package_list'),
    path('packages/create/', views.admin_package_create, name='package_create'),
    path('packages/<int:pk>/edit/', views.admin_package_edit, name='package_edit'),
    path('packages/<int:pk>/delete/', views.admin_package_delete, name='package_delete'),

    # Manajemen Pemesanan Paket
    path('bookings/', views.admin_booking_list, name='booking_list'),
    path('bookings/<int:pk>/status/', views.admin_booking_update_status, name='booking_update'),
]

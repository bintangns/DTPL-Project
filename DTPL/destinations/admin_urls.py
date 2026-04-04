from django.urls import path
from . import views

app_name = 'destinations_admin'

urlpatterns = [
    path('', views.admin_destination_list, name='list'),
    path('create/', views.admin_destination_create, name='create'),
    path('<int:pk>/edit/', views.admin_destination_edit, name='edit'),
    path('<int:pk>/delete/', views.admin_destination_delete, name='delete'),
]

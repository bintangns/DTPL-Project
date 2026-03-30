from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.admin_login, name='login'),
    path('dashboard/', views.admin_home, name='home'),
]
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('<slug:slug>/order/', views.product_order_create, name='order_create'),
    path('order/<int:pk>/success/', views.product_order_success, name='order_success'),
]
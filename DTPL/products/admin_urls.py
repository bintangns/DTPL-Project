from django.urls import path
from . import views

app_name = 'products_admin'

urlpatterns = [
    path('', views.admin_product_list, name='list'),
    path('create/', views.admin_product_create, name='create'),
    path('<int:pk>/edit/', views.admin_product_edit, name='edit'),
    path('<int:pk>/delete/', views.admin_product_delete, name='delete'),

    path('categories/', views.admin_category_list, name='category_list'),
    path('categories/create/', views.admin_category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.admin_category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.admin_category_delete, name='category_delete'),
]
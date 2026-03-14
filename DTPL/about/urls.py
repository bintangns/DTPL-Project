from django.urls import path
from . import views

app_name = 'about'

urlpatterns = [
    path('ecotourism/', views.ecotourism, name='ecotourism'),
]
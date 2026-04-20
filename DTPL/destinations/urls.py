from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list, name='list'),
    path('api/ask-gemini/', views.ask_gemini, name='ask_gemini'),
    path('<slug:slug>/', views.destination_detail, name='detail'),
]

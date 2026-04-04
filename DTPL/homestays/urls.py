from django.urls import path
from . import views

app_name = "homestays"

urlpatterns = [
    path("", views.homestay_list, name="list"),
    path("<slug:slug>/", views.homestay_detail, name="detail"),
]
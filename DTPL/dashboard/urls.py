from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('analytics/export/excel/', views.export_excel, name='export_excel'),
    path('analytics/export/pdf/', views.export_pdf, name='export_pdf'),
]

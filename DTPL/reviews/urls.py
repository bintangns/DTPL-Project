from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('admin/list/', views.admin_review_list, name='admin_list'),
    # path('admin/<int:review_id>/approve/', views.approve_review, name='approve'),
    path('admin/<int:review_id>/delete/', views.delete_review, name='delete'),
    path('admin/<int:review_id>/reply/', views.reply_review, name='reply'),

    path('<str:content_type>/<slug:slug>/', views.create_review, name='create'),
]
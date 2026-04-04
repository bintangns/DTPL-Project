"""
URL configuration for DTPL project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('django-admin/', admin.site.urls),

    # URL Admin
    path('admin/', include('adminpanel.urls')),
    path('admin/dashboard/', include('dashboard.urls')),
    path('admin/products/', include('products.admin_urls')),
    path('admin/destinations/', include('destinations.admin_urls')),
    path('admin/homestays/', include('homestays.admin_urls')),

    path('', include('home.urls')),
    path('destinasi/', include('destinations.urls')),
    path('products/', include('products.urls')),
    path('homestays/', include('homestays.urls')),
    path('about/', include('about.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
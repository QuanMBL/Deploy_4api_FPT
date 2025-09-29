"""
URL configuration for productapi project.
"""
from django.contrib import admin
from django.urls import path, include
from products.metrics_views import metrics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', include('products.urls')),
    path('metrics', metrics_view, name='metrics'),
]

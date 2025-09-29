"""
URL configuration for orderapi project.
"""
from django.contrib import admin
from django.urls import path, include
from orders.metrics_views import metrics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/orders/', include('orders.urls')),
    path('metrics', metrics_view, name='metrics'),
]

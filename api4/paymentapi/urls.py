"""
URL configuration for paymentapi project.
"""
from django.contrib import admin
from django.urls import path, include
from payments.metrics_views import metrics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/payments/', include('payments.urls')),
    path('metrics', metrics_view, name='metrics'),
]

"""
URL configuration for userapi project.
"""
from django.contrib import admin
from django.urls import path, include
from users.metrics_views import metrics_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('metrics', metrics_view, name='metrics'),
    
]

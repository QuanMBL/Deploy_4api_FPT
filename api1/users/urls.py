from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .metrics_views import metrics_view

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('metrics', metrics_view, name='metrics'),
]

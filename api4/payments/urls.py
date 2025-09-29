from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet
from .metrics_views import metrics_view

router = DefaultRouter()
router.register(r'', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('metrics', metrics_view, name='metrics'),
]

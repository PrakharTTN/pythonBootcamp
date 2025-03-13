from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserOrderModelViewSet

router = DefaultRouter()
router.register(r"orders", UserOrderModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

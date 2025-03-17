from django.urls import path, include
from rest_framework.routers import DefaultRouter
from basic import views as basic_views
from .views import UserOrderModelViewSet


router = DefaultRouter()
router.register(r"orders", UserOrderModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "menu/",
        basic_views.StaffItemView.as_view(),
        {"action": "GET"},
        name="view_menu",
    ),
]

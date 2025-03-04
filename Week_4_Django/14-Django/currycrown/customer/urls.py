from django.urls import path
from . import views

app_name = "customer"

urlpatterns = [
    path("view/", views.view_menu, name="view_menu"),
    path("place_order/", views.place_order, name="place_order"),
    path(
        "order_confirmation/<int:order_id>/",
        views.order_confirmation,
        name="order_confirmation",
    ),
]

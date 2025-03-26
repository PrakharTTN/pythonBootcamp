from django.urls import path
from .views import StaffItemView

urlpatterns = [
    path("items/", StaffItemView.as_view(), name="staff_item"),  # For POST AND GET
    path(
        "items/<int:id>", StaffItemView.as_view(), name="staff_update"
    ),  # FOR PUT,PATCH,DELETE
]

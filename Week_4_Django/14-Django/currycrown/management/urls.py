from django.urls import path
from . import views

app_name = "management"  

urlpatterns = []

menu_task = [
    path("add/", views.add_menu_item, name="add_menu_item"),
    path("view/", views.view_menu, name="view_menu"),
    path("specificmenu/", views.specific_view_menu, name="specific_view_menu"),
    path("remove/<int:item_id>/", views.remove_menu_item, name="remove_menu_item"),
    path("update/<int:item_id>/", views.update_menu, name="update_menu"),
]

order_task = [
    path("order/", views.show_orders, name="show_orders"),
    path("order/approve/<int:order_id>/", views.approve_order, name="approve_order"),
]
urlpatterns = urlpatterns + menu_task + order_task

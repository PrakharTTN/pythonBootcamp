from . import views
from django.urls import path

urlpatterns = [
    path("pollapp/", views.get, name="poll"),
]

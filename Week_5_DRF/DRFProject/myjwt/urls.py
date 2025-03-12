from django.urls import path, include
from rest_framework_simplejwt import views as jwtviews

urlpatterns = [
    path("login/token/", jwtviews.TokenObtainPairView.as_view(), name="obtain_token"),
    path(
        "login/token/refresh", jwtviews.TokenRefreshView.as_view(), name="refresh_token"
    ),
]

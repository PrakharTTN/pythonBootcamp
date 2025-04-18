"""
URL configuration for currycrown project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# from django.contrib import views as auth_views
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from . import views
from debug_toolbar.toolbar import debug_toolbar_urls
from django.shortcuts import redirect

urlpatterns = [
    path("admin/", admin.site.urls),
    path("logout", views.user_logout, name="logout"),
    path("management/", include("management.urls")),
    path("customer/", include("customer.urls")),
    path("register/", views.register, name="register_user"),
    path("login/", views.user_login, name="login"),
    path("", views.about, name="landing_page"),
    re_path(r"^.*$", lambda request: redirect("landing_page")),
] + debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

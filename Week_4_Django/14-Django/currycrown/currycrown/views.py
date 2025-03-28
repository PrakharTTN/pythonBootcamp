from django.shortcuts import render, redirect, reverse
from management.models import Menu
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import logout


def about(request):
    return render(request, "about.html")


def user_logout(request):
    logout(request)
    return redirect("landing_page")


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect("landing_page")
            else:
                return redirect("customer:view_menu")
    if request.user.is_authenticated:
        return redirect("landing_page")
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

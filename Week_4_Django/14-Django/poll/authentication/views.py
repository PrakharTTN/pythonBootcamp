from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = "auth/login.html"


class SignUpView(FormView):
    template_name = "auth/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")  # Redirect to login after successful signup

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = "/"

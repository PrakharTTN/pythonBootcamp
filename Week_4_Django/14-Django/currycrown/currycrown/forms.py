from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "placeholder": "First Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "placeholder": "Last Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Email Address",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Username",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already taken.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setting placeholder for password1 and password2 explicitly
        self.fields["password1"].widget.attrs.update(
            {
                "placeholder": "Enter Password",
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "placeholder": "Confirm Password",
            }
        )

"""Include neccessary imports"""

from django import forms
from .models import Menu
from django.core.exceptions import ValidationError


class MenuForm(forms.ModelForm):
    """Class to create menu form"""

    class Meta:
        """This defines the form's layout"""

        model = Menu
        fields = ["item_name", "item_price", "item_desc", "item_rating", "item_image"]

    def clean_item_name(self):
        item_name = self.cleaned_data.get("item_name")
        if Menu.objects.filter(item_name=item_name).exists():
            raise ValidationError("Menu Item Exists")
        return item_name


class MenuForm(forms.ModelForm):
    """Class to create menu form"""

    class Meta:
        """This defines the form's layout"""

        model = Menu
        fields = ["item_name", "item_price", "item_desc", "item_rating", "item_image"]

    def clean_item_name(self):
        item_name = self.cleaned_data.get("item_name")
        if Menu.objects.filter(item_name=item_name).exists():
            raise ValidationError("Menu Item Exists")
        return item_name

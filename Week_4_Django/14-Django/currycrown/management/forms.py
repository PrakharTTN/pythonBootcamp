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

    def clean_item_image(self):
        limit = 5 * 1024 * 1024
        item_image = self.cleaned_data.get("item_image")
        print(item_image.size)

        if item_image:
            if item_image.size > limit:
                raise ValidationError("Image size should not exceed 5MB.")

            if not item_image.name.endswith(("jpg", "png")):
                raise ValidationError(
                    "Invalid Image Format. Only jpg and png are allowed."
                )

        return item_image


class UpdateMenuForm(MenuForm):

    def clean_item_name(self):
        item_name = self.cleaned_data.get("item_name")
        return item_name.title()

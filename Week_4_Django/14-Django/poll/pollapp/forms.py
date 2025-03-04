from django import forms
from .models import Menu


class QuestionForm(forms.ModelForm):
    """Class to create menu form"""

    class Meta:
        """This defines the form's layout"""

        model = Menu
        fields = ["description", "answer"]

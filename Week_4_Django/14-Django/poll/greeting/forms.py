from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    """Class to create menu form"""

    class Meta:
        """This defines the form's layout"""

        model = Question
        fields = ["description", "answer"]

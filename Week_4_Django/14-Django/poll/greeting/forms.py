from django import forms
from django.core.exceptions import ValidationError
from .models import Vote


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["poll", "user"]


class UploadExcelForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if file.size > 10 * 1024 * 1024:  # size to be 10MB
            raise ValidationError("File size must be under 10 MB.")

        if not file.name.endswith(".xlsx"):  # should be xlsx file
            raise ValidationError("Only .xlsx files are allowed.")

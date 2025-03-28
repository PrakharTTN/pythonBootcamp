from django import forms
from .models import QuestionModel, ChoiceModel
from django.core.exceptions import ValidationError


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ["question_text"]

    def clean_question_text(self):
        text = self.cleaned_data.get("question_text")
        if QuestionModel.objects.filter(question_text__iexact=text).exists():
            raise ValidationError(message="Question Exists")
        return text


# To allow multiple choices to be added with the question, used a formset for ChoiceModel.
ChoiceFormSet = forms.modelformset_factory(ChoiceModel, fields=["choice"], extra=3)

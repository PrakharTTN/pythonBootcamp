from django.db import models
from datetime import date

CHOICES = [
    ("yes", "yes"),
    ("no", "no"),
]


class QuestionModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=date.today)


class ChoiceModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="choice"
    )
    choice = models.CharField(choices=CHOICES, max_length=3)
    votes = models.BigIntegerField(default=0)

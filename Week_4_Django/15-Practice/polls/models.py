from django.db import models
from datetime import date
from django.utils import timezone


class QuestionModel(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.question_text


class ChoiceModel(models.Model):
    question = models.ForeignKey(
        QuestionModel, on_delete=models.CASCADE, related_name="choice"
    )
    choice = models.CharField(max_length=20)
    votes = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.question.question_text} - {self.choice.title()}"

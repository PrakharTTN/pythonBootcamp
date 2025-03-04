from django.db import models

ANSWER_CHOICES = [("yes", "yes"), ("no", "no")]


# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    answer = models.CharField(choices=ANSWER_CHOICES)

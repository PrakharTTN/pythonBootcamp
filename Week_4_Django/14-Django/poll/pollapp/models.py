from django.db import models


# Create your models here.
class Question(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    answer = models.CharField(choices=[("yes", "yes"), ("no", "no")], max_length=3)

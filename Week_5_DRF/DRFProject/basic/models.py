from django.db import models
from .validators import validate_name, validate_number, validate_quantity


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, validators=[validate_name])
    description = models.TextField()
    price = models.IntegerField(validators=[validate_number])
    quantity = models.IntegerField(
        default=1, validators=[validate_number, validate_quantity]
    )

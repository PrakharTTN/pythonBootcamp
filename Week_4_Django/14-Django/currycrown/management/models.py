from django.db import models


class Menu(models.Model):
    """Menu Model"""

    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to="image")
    item_desc = models.TextField()
    item_price = models.PositiveBigIntegerField()
    item_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)

    def __str__(self):
        return self.item_name

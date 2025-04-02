from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

ORDER_STATUS_CHOICES = [
    ("pending", "pending"),
    ("complete", "complete"),
    ("cancelled", "cancelled"),
]


class Orders(models.Model):
    """This Model is to create orders based with foreign key of user"""

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    order_details = models.JSONField()
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="pending",
    )
    total_price = models.BigIntegerField(default=0)
    order_time = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.order_id} - Status: {self.order_status}"

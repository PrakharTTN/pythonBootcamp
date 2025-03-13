from django.db import models
from django.contrib.auth.models import User
from basic.models import Item


class UserOrderModel(models.Model):
    """This model stores the all the orders of all the user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through="OrderItem")
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"

    def calculate_total(self):
        """Method to calculate the total price for the order by adding the the price of each item
        and considering the quantity ordered"""

        self.total_price = sum(
            order_item.item.price * order_item.quantity
            for order_item in self.orderitem_set.all()
        )
        self.save()


class OrderItem(models.Model):
    """Intermediate model for the ManyToMany relationship between UserOrderModel and Item"""

    order = models.ForeignKey(UserOrderModel, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order {self.order.id}"

from rest_framework import serializers
from .models import UserOrderModel, OrderItem
from basic.models import Item
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for Item model"""

    class Meta:
        model = Item
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model (Model for MtoM Relationship)"""

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]


class UserOrderModelSerializer(serializers.ModelSerializer):
    """Serializer for UserOrderModel"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    orderitems = OrderItemSerializer(source="orderitem_set", many=True)
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserOrderModel
        fields = ["id", "user", "orderitems", "order_date", "total_price"]

    def create(self, validated_data):
        orderitems_data = validated_data.pop(
            "orderitem_set"
        )  # Get the data from the source field
        order = UserOrderModel.objects.create(**validated_data)

        for item_data in orderitems_data:
            item = item_data["item"]
            quantity = item_data["quantity"]
            if item.quantity < quantity:
                raise ValidationError(
                    f"Not enough stock for {item.name}. Available: {item.quantity}, Requested: {quantity}"
                )
            item.quantity -= quantity
            item.save()
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        order.calculate_total()
        return order

from rest_framework import serializers
from .models import UserOrderModel, OrderItem
from basic.models import Item
from django.contrib.auth.models import User


# class ItemSerializer(serializers.ModelSerializer):
#     """Serializer for Item model"""

#     class Meta:
#         model = Item
#         fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model (Mid- Model for MtoM Relationship)"""

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]

class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model (Mid- Model for MtoM Relationship)"""
    
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ["item", "quantity"]


class UserOrderModelSerializer(serializers.ModelSerializer):
    """Serializer for UserOrderModel"""

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    items = OrderItemSerializer(many=True)
    total_price = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserOrderModel
        fields = ["id", "user", "items", "order_date", "total_price"]

    def create(self, validated_data):
        """Handle creation of UserOrderModel and OrderItems"""
        items_data = validated_data.pop("items")
        order = UserOrderModel.objects.create(**validated_data)

        # Iterate over items_data, where "item" is now the full Item object, not just the ID
        for item_data in items_data:
            item = item_data["item"]  # This is an actual Item object
            quantity = item_data["quantity"]

            # Ensure that we're passing the item ID to the OrderItem
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        order.calculate_total()
        return order

    def update(self, instance, validated_data):
        """Handle updating of the UserOrderModel and OrderItems"""

        items_data = validated_data.pop("items", None)
        instance.user = validated_data.get("user", instance.user)

        instance.save()

        if items_data is not None:
            # Remove existing OrderItems and add new ones
            instance.items.clear()
            for item_data in items_data:
                item = item_data["item"]
                quantity = item_data["quantity"]
                OrderItem.objects.create(order=instance, item=item, quantity=quantity)

        instance.calculate_total()  # Recalculate total price after update
        return instance

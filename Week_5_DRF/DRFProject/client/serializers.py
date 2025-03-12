from rest_framework import serializers
from .models import UserOrderModel, Item, OrderItem
from django.contrib.auth.models import User

# Serializer for Item model
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

# Serializer for OrderItem model (Intermediate Model for Many-to-Many Relationship)
class OrderItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()  # Nesting ItemSerializer to include item details in the response

    class Meta:
        model = OrderItem
        fields = ['item', 'quantity']

# Serializer for UserOrderModel
class UserOrderModelSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Linking to User model
    items = OrderItemSerializer(many=True)  # Nested OrderItemSerializer to handle the items in the order
    total_price = serializers.IntegerField(read_only=True)  # We can calculate total_price dynamically

    class Meta:
        model = UserOrderModel
        fields = ['id', 'user', 'items', 'order_date', 'total_price']

    def create(self, validated_data):
        # Handle creation of UserOrderModel and OrderItems
        items_data = validated_data.pop('items')
        order = UserOrderModel.objects.create(**validated_data)

        # Create OrderItem instances
        for item_data in items_data:
            item = item_data['item']
            quantity = item_data['quantity']
            OrderItem.objects.create(order=order, item=item, quantity=quantity)

        order.calculate_total()  # Calculate total price for the order
        return order

    def update(self, instance, validated_data):
        # Handle updating of the UserOrderModel and OrderItems
        items_data = validated_data.pop('items', None)
        instance.user = validated_data.get('user', instance.user)

        instance.save()

        if items_data is not None:
            # Remove existing OrderItems and add new ones
            instance.items.clear()
            for item_data in items_data:
                item = item_data['item']
                quantity = item_data['quantity']
                OrderItem.objects.create(order=instance, item=item, quantity=quantity)

        instance.calculate_total()  # Recalculate total price after update
        return instance

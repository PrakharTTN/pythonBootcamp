from django.db import models
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """This class is to serialize the ITEM DB data"""

    def validate(self, data):
        """This method validates the data based on the ITEM_NAME if it exists"""

        if Item.objects.filter(name=data["name"]).exists():
            raise serializers.ValidationError("Item already exists")
        return data

    class Meta:
        model = Item
        fields = ["name", "description", "price", "quantity"]


class UpdateItemSerializer(ItemSerializer):
    """This class is to override the validation of serializer when updating name"""

    def validate(self, data):
        return data

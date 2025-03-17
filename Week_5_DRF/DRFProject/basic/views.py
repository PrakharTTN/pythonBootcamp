from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer, UpdateItemSerializer


class StaffItemView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """This Function is to POST data in DB"""

        data = ItemSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(
                {"Message": "Object Creation Successful"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"Message": "Object Creation Failed", "Errors": data.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, *args, **kwargs):
        """This Function is to GET data in DB"""

        model_data = Item.objects.all().order_by("id")
        if model_data:
            mydata = ItemSerializer(model_data, many=True)
            return Response(mydata.data)
        return Response(
            {"Message": "Table is empty"}, status=status.HTTP_204_NO_CONTENT
        )

    def put(self, request, name, *args, **kwargs):
        """This function is to PUT data in DB"""

        item = get_object_or_404(Item, name=name)

        serialize = UpdateItemSerializer(item, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(
                {"message": "Item Successfully Updated"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"Errors": serialize.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, name, *args, **kwargs):
        """This function is to PUT data in DB"""

        item = get_object_or_404(Item, name=name)

        serialize = UpdateItemSerializer(item, data=request.data)
        if serialize.is_valid():
            serialize.save()
            return Response(
                {"message": "Item Successfully Updated"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"Errors": serialize.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, name, *args, **kwargs):
        """This function is to DELETE data in DB."""
        item = get_object_or_404(Item, name=name)
        item.delete()
        return Response({"message": "Item deleted successfully"})

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import UserOrderModel
from .serializers import UserOrderModelSerializer
from rest_framework.permissions import IsAuthenticated


class UserOrderModelViewSet(viewsets.ModelViewSet):
    queryset = UserOrderModel.objects.all()
    serializer_class = UserOrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Optionally restricts the returned orders to the current user,
        by filtering against a user query parameter in the URL."""

        user = self.request.user
        print(f"Filtering orders for user: {user.username}")
        return UserOrderModel.objects.filter(user=user)
        

    def create(self, request, *args, **kwargs):
        """Overriding the create method to handle the creation of UserOrderModel
        and associated OrderItem model instances."""

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(
                self.get_serializer(order).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """Retrieve a specific order, including the associated items"""

        order = self.get_object()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

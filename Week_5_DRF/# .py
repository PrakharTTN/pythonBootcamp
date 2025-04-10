# .txt

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError


class ItemSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100,validators=[UniqueValidator(queryset=Item.objects.all()) ])
    class Meta:
        # model=Item
        fields='__all__'
    def validate_phone(self, value):
        if Item.objects.filter(phone=value).exists():
            raise ValidationError(message="Phone already exists")



from django import forms

class UserInputForm(forms.Form):
    name=forms.CharField()
    age=forms.IntegerField()
    image=forms.ImageField(validators=[validate_image])
    
    def validate_image(self, image):
        limit = 5*1024*1024
        if image.size > limit:
            raise ValidationError(message="image size too big")
        
from django.db import models

class ItemModel(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to="/image")

    def __str__(self):
        return self.name
    
    def clean(self):
        limit=5*1024*1024
        if self.image.size<limit:
            raise ValidationError
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args,**kwargs)


from rest_framework import views
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
class ItemViewSet(viewsets.ModelViewSet):

    serializer_class="abc"
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        user=self.request.user
        print(f"filtering for{user.username}")
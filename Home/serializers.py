from rest_framework import serializers
from .models import Stock, User
from django.contrib.auth import get_user_model
class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ["symbol", "name", "price", "last_updated"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
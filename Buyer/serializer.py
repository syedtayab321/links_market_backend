from rest_framework import serializers
from .models import (
    BuyerSignUp, TaskCreation, Order, BuyerProfile, Escrow
)


class BuyerSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerSignUp
        fields = ['id', 'username', 'email', 'company_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        buyer = BuyerSignUp(**validated_data)
        buyer.set_password(password)  # Use Django's set_password method for hashing
        buyer.save()
        return buyer


class TaskSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TaskCreation
        fields = ['id', 'buyer', 'title', 'description', 'budget', 'deadline', 'status']


class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)
    product = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'buyer', 'product', 'quantity', 'price', 'status', 'ordered_at']


class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['id', 'buyer', 'address', 'phone_number', 'company_details']


class EscrowSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Escrow
        fields = ['id', 'buyer', 'order', 'amount', 'status', 'created_at']


class PerformanceAnalyticsSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)

    class Meta:
        #model = PerformanceAnalytics
        fields = ['id', 'buyer', 'impressions', 'views', 'orders', 'sales_percentage', 'ranking']

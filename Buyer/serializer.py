from rest_framework import serializers
from .models import BuyerSignUp, TaskCreation


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
        buyer.password = password
        buyer.save()
        return buyer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCreation
        fields = ['id', 'buyer', 'title', 'description', 'budget', 'deadline', 'status']

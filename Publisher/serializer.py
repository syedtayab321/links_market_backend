from rest_framework import serializers
from Publisher import models as publisherModels
from .utils import send_verification_email


class PublisherSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisherModels.PublisherSingUp
        fields = ['id', 'username', 'email', 'password', 'website', 'is_verified']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_verified': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        publisher = publisherModels.PublisherSingUp(**validated_data)
        publisher.password = password
        publisher.generate_verification_code()
        send_verification_email(publisher.email, publisher.verification_code)  # Send email
        publisher.save()
        return publisher


class PerformanceAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisherModels.PerformanceAnalytics
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisherModels.Task
        fields = '__all__'


class WebsiteListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisherModels.WebsiteListing
        fields = '__all__'


class BulkUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = publisherModels.BulkUpload
        fields = '__all__'

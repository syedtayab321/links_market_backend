from rest_framework.decorators import api_view
from rest_framework.response import Response
from link_market_backend.Publisher import models as PublisherModels
from link_market_backend.Publisher import serializer as PublisherSerializer
import os
from django.conf import settings
from rest_framework import status
import csv
from io import TextIOWrapper
from rest_framework.parsers import MultiPartParser


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def PublisherSignUp(request):
    if request.method == 'GET':
        try:
            publishers = PublisherModels.PublisherSingUp.objects.all()
            serializer = PublisherSerializer.PublisherSignUpSerializer(publishers, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': 'No data found', 'details': str(e)}, status=404)

    elif request.method == 'POST':
        serializer = PublisherSerializer.PublisherSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Publisher created successfully', 'data': serializer.data})
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)

    elif request.method == 'PUT':
        try:
            publisher_id = request.data.get('id')
            publisher = PublisherModels.PublisherSingUp.objects.get(id=publisher_id)
            serializer = PublisherSerializer.PublisherSignUpSerializer(publisher, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Publisher updated successfully', 'data': serializer.data})
            return Response({'error': 'Invalid data', 'details': serializer.errors}, status=400)
        except PublisherModels.PublisherSingUp.DoesNotExist:
            return Response({'error': 'Publisher not found'}, status=404)
        except Exception as e:
            return Response({'error': 'An error occurred', 'details': str(e)}, status=500)

    elif request.method == 'DELETE':
        try:
            publisher_id = request.GET.get('id')
            if not publisher_id:
                return Response({'error': 'ID parameter is required'}, status=400)
            PublisherModels.PublisherSingUp.objects.filter(id=publisher_id).delete()
            return Response({'message': 'Publisher deleted successfully'})
        except Exception as e:
            return Response({'error': 'An error occurred', 'details': str(e)}, status=500)


@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    code = request.data.get('verification_code')

    if not email or not code:
        return Response({'error': 'Email and verification code are required'}, status=400)

    try:
        publisher = PublisherModels.PublisherSingUp.objects.get(email=email, verification_code=code)
        publisher.is_verified = True
        publisher.verification_code = None
        publisher.save()
        return Response({'message': 'Email verified successfully'})
    except PublisherModels.PublisherSingUp.DoesNotExist:
        return Response({'error': 'Invalid email or verification code'}, status=400)


# Task Management Views
@api_view(['GET', 'POST'])
def task_list(request):
    if request.method == 'GET':
        tasks = PublisherModels.Task.objects.all()
        serializer = PublisherSerializer.TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PublisherSerializer.TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task = PublisherModels.Task.objects.get(pk=pk)
    except PublisherModels.Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PublisherSerializer.TaskSerializer(task)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PublisherSerializer.TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Listings Views
@api_view(['GET', 'POST'])
def listing_list(request):
    if request.method == 'GET':
        listings = PublisherModels.WebsiteListing.objects.all()
        serializer = PublisherSerializer.WebsiteListingSerializer(listings, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PublisherSerializer.WebsiteListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def listing_detail(request, pk):
    try:
        listing = PublisherModels.WebsiteListing.objects.get(pk=pk)
    except PublisherModels.WebsiteListing.DoesNotExist:
        return Response({'error': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PublisherSerializer.WebsiteListingSerializer(listing)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PublisherSerializer.WebsiteListingSerializer(listing, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        listing.delete()
        return Response({'message': 'Listing deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Performance Analytics Views
@api_view(['GET'])
def performance_analytics(request):
    analytics = PublisherModels.PerformanceAnalytics.objects.all()
    serializer = PublisherSerializer.PerformanceAnalyticsSerializer(analytics, many=True)
    return Response(serializer.data)


# Bulk Upload Views
@api_view(['POST'])
def bulk_upload(request):
    """
    Handle bulk website uploads via CSV. The CSV should have a 'website_url' column.
    """
    parser_classes = [MultiPartParser]

    if 'file' not in request.FILES:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

    file = request.FILES['file']
    if not file.name.endswith('.csv'):
        return Response({'error': 'Only CSV files are supported'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = TextIOWrapper(file.file, encoding='utf-8')
        csv_reader = csv.DictReader(data)

        listings = []
        for row in csv_reader:
            website_url = row.get('website_url')

            if not website_url:
                return Response({'error': 'Missing website_url in one or more rows'},
                                status=status.HTTP_400_BAD_REQUEST)
            listings.append(PublisherModels.WebsiteListing(user=request.user, website_url=website_url, verified=False))
        Listing.objects.bulk_create(listings)

        return Response({'message': f'{len(listings)} listings uploaded successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

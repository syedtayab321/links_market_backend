from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import BuyerSignUp, TaskCreation, Order, Escrow
from .serializer import (
    BuyerSignUpSerializer,
    TaskSerializer,
    OrderSerializer,
    BuyerProfileSerializer,
    EscrowSerializer,
    PerformanceAnalyticsSerializer
)

# Buyer SignUp View
class BuyerSignUpView(generics.CreateAPIView):
    queryset = BuyerSignUp.objects.all()
    serializer_class = BuyerSignUpSerializer


# Buyer Profile View
class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user
        serializer = BuyerProfileSerializer(buyer)
        return Response(serializer.data)

    def put(self, request):
        buyer = request.user
        serializer = BuyerProfileSerializer(buyer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Task Creation View
class TaskCreateView(generics.CreateAPIView):
    queryset = TaskCreation.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


# Task List View
class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskCreation.objects.filter(buyer=self.request.user)


# Order Creation View
class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


# Order List View
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


# Escrow Creation View
class EscrowCreateView(generics.CreateAPIView):
    queryset = Escrow.objects.all()
    serializer_class = EscrowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


# Escrow List View
class EscrowListView(generics.ListAPIView):
    serializer_class = EscrowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Escrow.objects.filter(buyer=self.request.user)


# Performance Analytics View
class PerformanceAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user
        analytics, created = PerformanceAnalytics.objects.get_or_create(buyer=buyer)
        serializer = PerformanceAnalyticsSerializer(analytics)
        return Response(serializer.data)

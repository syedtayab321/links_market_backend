from django.urls import path
from Buyer.views import (
    BuyerSignUpView, BuyerProfileView, TaskCreateView, TaskListView, 
    OrderCreateView, OrderListView, EscrowCreateView, EscrowListView, 
    PerformanceAnalyticsView
)

urlpatterns = [
    # Authentication (Sign Up)
    path('signup/', BuyerSignUpView.as_view(), name='buyer_signup'),

    # Profile
    path('profile/', BuyerProfileView.as_view(), name='buyer_profile'),

    # Tasks
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/list/', TaskListView.as_view(), name='task_list'),

    # Orders
    path('orders/create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/list/', OrderListView.as_view(), name='order_list'),

    # Escrows
    path('escrows/create/', EscrowCreateView.as_view(), name='escrow_create'),
    path('escrows/list/', EscrowListView.as_view(), name='escrow_list'),

    # Performance Analytics
    path('analytics/performance/', PerformanceAnalyticsView.as_view(), name='performance_analytics'),
]

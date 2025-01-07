from django.urls import path
from link_market_backend.Publisher import  views

urlpatterns = [
    path('publisherSignUp/', views.PublisherSignUp, name='publishers-singUp'),
    path('publisherSignUp/verify-email/', views.verify_email, name='verify-email'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:pk>/', views.task_detail, name='task-detail'),
    path('listings/', views.listing_list, name='listing-list'),
    path('listings/<int:pk>/', views.listing_detail, name='listing-detail'),
    path('analytics/', views.performance_analytics, name='performance-analytics'),
    path('bulk-upload/', views.bulk_upload, name='bulk-upload'),
]

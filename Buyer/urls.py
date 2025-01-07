from django.urls import path
from link_market_backend.Buyer import views

urlpatterns = [
    path('buyersSingup/', views.BuyersSignUp, name='buyers-signup'),
    path('tasks/', views.TasksData, name='tasks-data'),
]

"""
Payment app URL configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.list_plans, name='list_plans'),
    path('create-order/', views.create_order, name='create_order'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('subscription-status/', views.subscription_status, name='subscription_status'),
]

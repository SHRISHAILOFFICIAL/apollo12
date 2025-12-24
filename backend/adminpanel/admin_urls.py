"""
Admin panel URL configuration
"""
from django.urls import path
from . import admin_views

urlpatterns = [
    path('dashboard/stats/', admin_views.dashboard_stats, name='dashboard_stats'),
    path('payments/failures/', admin_views.payment_failures, name='payment_failures'),
    path('exams/issues/', admin_views.exam_issues, name='exam_issues'),
]

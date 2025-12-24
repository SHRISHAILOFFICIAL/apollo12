"""
Admin panel views for analytics and monitoring
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import timedelta

from payments.models import Payment, Subscription, Plan
from users.models import User, UserActivity
from results.models import Attempt
from exams.models import Exam


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin
    
    GET /api/admin/dashboard/stats/
    """
    now = timezone.now()
    
    # Active users (last 24h, 7d, 30d)
    active_24h = UserActivity.objects.filter(
        created_at__gte=now - timedelta(hours=24)
    ).values('user').distinct().count()
    
    active_7d = UserActivity.objects.filter(
        created_at__gte=now - timedelta(days=7)
    ).values('user').distinct().count()
    
    active_30d = UserActivity.objects.filter(
        created_at__gte=now - timedelta(days=30)
    ).values('user').distinct().count()
    
    # Payment statistics
    total_revenue = Payment.objects.filter(
        status__in=['paid', 'activated']
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    successful_payments = Payment.objects.filter(
        status__in=['paid', 'activated']
    ).count()
    
    failed_payments = Payment.objects.filter(status='failed').count()
    
    # Recent revenue (last 30 days)
    recent_revenue = Payment.objects.filter(
        status__in=['paid', 'activated'],
        created_at__gte=now - timedelta(days=30)
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Subscription statistics
    active_subscriptions = Subscription.objects.filter(status='active').count()
    expired_subscriptions = Subscription.objects.filter(status='expired').count()
    
    # User tier breakdown (computed from active subscriptions)
    from django.db.models import Exists, OuterRef
    
    active_sub_exists = Subscription.objects.filter(
        user=OuterRef('pk'),
        status='active',
        end_date__gt=now
    )
    
    pro_users = User.objects.filter(Exists(active_sub_exists)).count()
    free_users = User.objects.exclude(Exists(active_sub_exists)).count()
    
    # Exam statistics
    total_attempts = Attempt.objects.count()
    completed_attempts = Attempt.objects.filter(status='submitted').count()
    active_attempts = Attempt.objects.filter(status='in_progress').count()
    
    return Response({
        'success': True,
        'stats': {
            'users': {
                'total': User.objects.count(),
                'pro': pro_users,
                'free': free_users,
                'active_24h': active_24h,
                'active_7d': active_7d,
                'active_30d': active_30d,
            },
            'payments': {
                'total_revenue_paisa': total_revenue,
                'total_revenue_rupees': total_revenue / 100,
                'recent_revenue_paisa': recent_revenue,
                'recent_revenue_rupees': recent_revenue / 100,
                'successful': successful_payments,
                'failed': failed_payments,
                'success_rate': round(successful_payments / (successful_payments + failed_payments) * 100, 2) if (successful_payments + failed_payments) > 0 else 0,
            },
            'subscriptions': {
                'active': active_subscriptions,
                'expired': expired_subscriptions,
            },
            'exams': {
                'total_attempts': total_attempts,
                'completed': completed_attempts,
                'active': active_attempts,
                'completion_rate': round(completed_attempts / total_attempts * 100, 2) if total_attempts > 0 else 0,
            }
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def payment_failures(request):
    """
    Get payment failure logs
    
    GET /api/admin/payments/failures/
    Query params:
    - limit: Number of records (default: 50)
    - days: Number of days to look back (default: 7)
    """
    limit = int(request.GET.get('limit', 50))
    days = int(request.GET.get('days', 7))
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    failed_payments = Payment.objects.filter(
        status='failed',
        created_at__gte=cutoff_date
    ).select_related('user').order_by('-created_at')[:limit]
    
    failures = []
    for payment in failed_payments:
        failures.append({
            'id': payment.id,
            'user': {
                'id': payment.user.id,
                'username': payment.user.username,
                'email': payment.user.email,
            },
            'amount': payment.amount,
            'amount_rupees': payment.amount / 100,
            'order_id': payment.order_id,
            'provider_payment_id': payment.provider_payment_id,
            'error_code': payment.metadata.get('error_code'),
            'error_description': payment.metadata.get('error_description'),
            'created_at': payment.created_at,
        })
    
    return Response({
        'success': True,
        'failures': failures,
        'count': len(failures),
        'period_days': days,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def exam_issues(request):
    """
    Get exam crash/timeout logs
    
    GET /api/admin/exams/issues/
    Query params:
    - limit: Number of records (default: 50)
    - days: Number of days to look back (default: 7)
    """
    limit = int(request.GET.get('limit', 50))
    days = int(request.GET.get('days', 7))
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    # Get incomplete attempts (potential crashes/timeouts)
    incomplete_attempts = Attempt.objects.filter(
        status='in_progress',
        started_at__lt=cutoff_date
    ).select_related('user', 'exam').order_by('-started_at')[:limit]
    
    issues = []
    for attempt in incomplete_attempts:
        # Calculate expected end time
        expected_end = attempt.started_at + timedelta(minutes=attempt.exam.duration_minutes)
        is_timeout = timezone.now() > expected_end
        
        issues.append({
            'id': attempt.id,
            'user': {
                'id': attempt.user.id,
                'username': attempt.user.username,
                'email': attempt.user.email,
            },
            'exam': {
                'id': attempt.exam.id,
                'name': attempt.exam.name,
                'year': attempt.exam.year,
            },
            'started_at': attempt.started_at,
            'expected_end': expected_end,
            'is_timeout': is_timeout,
            'duration_minutes': attempt.exam.duration_minutes,
        })
    
    return Response({
        'success': True,
        'issues': issues,
        'count': len(issues),
        'period_days': days,
    })

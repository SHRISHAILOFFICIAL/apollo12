"""
Custom middleware for subscription management and security
"""
import logging
from django.utils import timezone
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class SubscriptionExpiryMiddleware:
    """
    Middleware to check and auto-downgrade expired subscriptions
    Runs on every request to ensure subscription status is current
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check subscription expiry for authenticated users
        if hasattr(request, 'user') and request.user.is_authenticated:
            self.check_subscription_expiry(request.user)
        
        response = self.get_response(request)
        return response
    
    @staticmethod
    def check_subscription_expiry(user):
        """Check if user's subscription has expired and mark as expired"""
        try:
            # Get user's active subscriptions
            from payments.models import Subscription
            active_subscriptions = Subscription.objects.filter(
                user=user,
                status='active',
                end_date__lte=timezone.now()
            )
            
            # Mark expired subscriptions
            if active_subscriptions.exists():
                count = active_subscriptions.update(status='expired')
                logger.info(f"Marked {count} subscription(s) as expired for user {user.username}")
        
        except Exception as e:
            logger.error(f"Error checking subscription expiry for user {user.id}: {str(e)}")


class ActiveExamSessionMiddleware:
    """
    Middleware to prevent multiple logins during active exam attempts
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check for active exam sessions on exam-related endpoints
        if hasattr(request, 'user') and request.user.is_authenticated:
            if self.is_exam_endpoint(request.path):
                has_active_session, session_info = self.check_active_exam_session(request.user, request)
                
                if has_active_session and not self.is_same_session(request, session_info):
                    return JsonResponse({
                        'success': False,
                        'error': 'You have an active exam session in another browser/tab. Please complete or close that session first.',
                        'active_session': {
                            'exam_id': session_info.get('exam_id'),
                            'started_at': session_info.get('started_at')
                        }
                    }, status=409)  # 409 Conflict
        
        response = self.get_response(request)
        return response
    
    @staticmethod
    def is_exam_endpoint(path):
        """Check if the request is for starting a new exam"""
        # Only check when starting a new exam attempt
        return '/api/exams/' in path and '/start' in path
    
    @staticmethod
    def check_active_exam_session(user, request):
        """
        Check if user has an active exam session
        
        Returns:
            tuple: (has_active_session: bool, session_info: dict)
        """
        try:
            from results.models import Attempt
            
            # Check for active exam attempts
            active_attempt = Attempt.objects.filter(
                user=user,
                status='in_progress'
            ).first()
            
            if active_attempt:
                return True, {
                    'exam_id': active_attempt.exam.id,
                    'started_at': active_attempt.started_at.isoformat(),
                    'session_token': getattr(active_attempt, 'session_token', None)
                }
            
            return False, {}
        
        except Exception as e:
            logger.error(f"Error checking active exam session: {str(e)}")
            return False, {}
    
    @staticmethod
    def is_same_session(request, session_info):
        """Check if the current request is from the same session"""
        # Compare session tokens if available
        request_session_token = request.headers.get('X-Session-Token')
        stored_session_token = session_info.get('session_token')
        
        if request_session_token and stored_session_token:
            return request_session_token == stored_session_token
        
        return False

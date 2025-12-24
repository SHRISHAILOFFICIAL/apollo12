"""
Custom rate limiting/throttling classes for API endpoints
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Rate limit for login attempts
    5 attempts per minute for anonymous users
    """
    rate = '5/min'
    scope = 'login'


class OTPRateThrottle(AnonRateThrottle):
    """
    Rate limit for OTP generation
    3 requests per 5 minutes
    """
    rate = '3/5min'
    scope = 'otp'


class PaymentRateThrottle(UserRateThrottle):
    """
    Rate limit for payment verification
    10 requests per minute for authenticated users
    """
    rate = '10/min'
    scope = 'payment'


class ExamStartRateThrottle(UserRateThrottle):
    """
    Rate limit for starting exams
    Prevents rapid exam attempt creation
    """
    rate = '5/min'
    scope = 'exam_start'

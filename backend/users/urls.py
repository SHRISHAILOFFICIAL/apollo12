from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthViewSet, NotificationViewSet, UserActivityViewSet,
    send_signup_otp, verify_signup_otp,
    send_password_reset_otp, verify_password_reset_otp, reset_password,
    submit_query
)

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'activities', UserActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
    # OTP endpoints
    path('send-signup-otp/', send_signup_otp, name='send-signup-otp'),
    path('verify-signup-otp/', verify_signup_otp, name='verify-signup-otp'),
    path('send-password-reset-otp/', send_password_reset_otp, name='send-password-reset-otp'),
    path('verify-password-reset-otp/', verify_password_reset_otp, name='verify-password-reset-otp'),
    path('reset-password/', reset_password, name='reset-password'),
    # Contact/Query endpoint
    path('submit-query/', submit_query, name='submit-query'),
]

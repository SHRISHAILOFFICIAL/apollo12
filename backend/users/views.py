from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.utils import timezone

from .models import User, Notification, UserActivity
from .tokens import RefreshToken
from .serializers import (
    SignupSerializer, LoginSerializer, UserSerializer,
    NotificationSerializer, UserActivitySerializer
)


class AuthViewSet(viewsets.ViewSet):
    """ViewSet for authentication endpoints"""
    
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def signup(self, request):
        """
        User signup endpoint
        POST /api/auth/signup/
        Body: {username, email, name, mobile, password, confirm_password}
        """
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Log activity
            UserActivity.objects.create(
                user=user,
                activity='User registered',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT')
            )
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        User login endpoint
        POST /api/auth/login/
        Body: {username, password}
        Note: username can be either username or email
        """
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = None
        
        try:
            # Step 1: Try to find user by username
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                # Step 2: If not found, try to find by email
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                # Step 3: If still not found, return error
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Step 4: Check password
        if not check_password(password, user.password_hash):
            # Step 5: If incorrect, return same error
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Step 6: Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        # Log activity
        UserActivity.objects.create(
            user=user,
            activity='User logged in',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        # Step 7: Return response
        return Response({
            'message': 'Login successful',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current user profile
        GET /api/auth/me/
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for user notifications"""
    
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for current user only"""
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        notifications = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().update(is_read=True)
        return Response({'message': 'All notifications marked as read'})


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing user activity logs"""
    
    serializer_class = UserActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return activity logs for current user only"""
        return UserActivity.objects.filter(user=self.request.user)


# OTP Verification Views
@api_view(['POST'])
def send_signup_otp(request):
    """
    Send OTP for email verification during signup
    POST /api/users/send-signup-otp/
    Body: {email}
    """
    from .models import EmailOTP
    from .email_service import generate_otp, send_otp_email
    from .disposable_emails import is_allowed_email
    
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if email is from an allowed provider
    if not is_allowed_email(email):
        return Response(
            {'error': 'Please use an email from a trusted provider (e.g., Gmail, Outlook, Yahoo). Temporary email addresses are not allowed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate OTP
    otp = generate_otp()
    
    # Save to database
    EmailOTP.objects.create(
        email=email,
        otp=otp,
        purpose='signup'
    )
    
    # Send email
    if send_otp_email(email, otp, purpose='signup'):
        return Response({
            'message': 'OTP sent successfully',
            'email': email
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Failed to send OTP. Please try again.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def verify_signup_otp(request):
    """
    Verify OTP for email verification during signup
    POST /api/users/verify-signup-otp/
    Body: {email, otp}
    """
    from .models import EmailOTP
    
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email or not otp:
        return Response(
            {'error': 'Email and OTP are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get the latest unverified OTP for this email
        otp_obj = EmailOTP.objects.filter(
            email=email,
            otp=otp,
            purpose='signup',
            is_verified=False
        ).latest('created_at')
        
        if otp_obj.is_valid():
            otp_obj.is_verified = True
            otp_obj.save()
            return Response({
                'message': 'Email verified successfully',
                'email': email
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'OTP has expired. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except EmailOTP.DoesNotExist:
        return Response(
            {'error': 'Invalid OTP'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def send_password_reset_otp(request):
    """
    Send OTP for password reset
    POST /api/users/send-password-reset-otp/
    Body: {email}
    """
    from .models import EmailOTP
    from .email_service import generate_otp, send_otp_email
    
    email = request.data.get('email')
    
    if not email:
        return Response(
            {'error': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if user exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Don't reveal if email exists or not for security
        return Response({
            'message': 'If this email is registered, you will receive a password reset code.',
            'email': email
        }, status=status.HTTP_200_OK)
    
    # Generate OTP
    otp = generate_otp()
    
    # Save to database
    EmailOTP.objects.create(
        email=email,
        otp=otp,
        purpose='password_reset'
    )
    
    # Send email
    send_otp_email(email, otp, purpose='password_reset')
    
    return Response({
        'message': 'If this email is registered, you will receive a password reset code.',
        'email': email
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_password_reset_otp(request):
    """
    Verify OTP for password reset (doesn't reset password yet, just verifies OTP)
    POST /api/users/verify-password-reset-otp/
    Body: {email, otp}
    """
    from .models import EmailOTP
    
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    if not email or not otp:
        return Response(
            {'error': 'Email and OTP are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Get the latest unverified OTP for this email
        otp_obj = EmailOTP.objects.filter(
            email=email,
            otp=otp,
            purpose='password_reset',
            is_verified=False
        ).latest('created_at')
        
        if otp_obj.is_valid():
            return Response({
                'message': 'OTP verified successfully. You can now reset your password.',
                'email': email,
                'otp': otp  # Return OTP for use in reset password step
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'OTP has expired. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )
    except EmailOTP.DoesNotExist:
        return Response(
            {'error': 'Invalid OTP'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
def reset_password(request):
    """
    Reset password after OTP verification
    POST /api/users/reset-password/
    Body: {email, otp, new_password}
    """
    from .models import EmailOTP
    
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')
    
    if not email or not otp or not new_password:
        return Response(
            {'error': 'Email, OTP, and new password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password length
    if len(new_password) < 6:
        return Response(
            {'error': 'Password must be at least 6 characters long'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Verify OTP one more time
        otp_obj = EmailOTP.objects.filter(
            email=email,
            otp=otp,
            purpose='password_reset',
            is_verified=False
        ).latest('created_at')
        
        if not otp_obj.is_valid():
            return Response(
                {'error': 'OTP has expired. Please request a new one.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user and reset password
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        
        # Mark OTP as verified
        otp_obj.is_verified = True
        otp_obj.save()
        
        # Log activity
        UserActivity.objects.create(
            user=user,
            activity='Password reset via OTP',
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT')
        )
        
        return Response({
            'message': 'Password reset successfully. You can now login with your new password.'
        }, status=status.HTTP_200_OK)
        
    except EmailOTP.DoesNotExist:
        return Response(
            {'error': 'Invalid OTP'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )


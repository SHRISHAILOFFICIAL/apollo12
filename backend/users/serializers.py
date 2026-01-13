from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from .models import User, PasswordResetRequest, UserActivity, Notification, Query
from .disposable_emails import is_allowed_email, get_allowed_domains_list


class SignupSerializer(serializers.Serializer):
    """Serializer for user signup - EXACTLY as specified"""
    
    username = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(required=True, max_length=150)
    name = serializers.CharField(required=True, max_length=150)
    mobile = serializers.CharField(required=True, max_length=20, min_length=10)
    password = serializers.CharField(required=True, write_only=True, min_length=6)
    confirm_password = serializers.CharField(required=True, write_only=True, min_length=6)
    
    def validate_username(self, value):
        """Validate username is unique"""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def validate_email(self, value):
        """Validate email is unique and from allowed provider"""
        # Check if email already exists
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        
        # Check if email is from an allowed provider (whitelist)
        if not is_allowed_email(value):
            allowed_providers = ['Gmail', 'Outlook', 'Yahoo', 'iCloud', 'ProtonMail', 'Zoho', 'AOL']
            raise serializers.ValidationError(
                f"Please use an email from a trusted provider (e.g., {', '.join(allowed_providers[:3])}, etc.). "
                "Temporary email addresses are not allowed."
            )
        
        return value
    
    def validate(self, data):
        """Validate password and confirm_password match"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })
        return data
    
    def create(self, validated_data):
        """Create user with hashed password"""
        # Remove confirm_password - never store it
        validated_data.pop('confirm_password')
        
        # Hash the password
        password_hash = make_password(validated_data.pop('password'))
        
        # Create user with auto-set fields
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            mobile=validated_data.get('mobile', ''),
            password_hash=password_hash,
            email_verified=False,
            mobile_verified=False,
            role='student',
            is_active=True
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login - ONLY username and password"""
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model - safe fields only"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'email_verified', 'is_staff', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email_verified', 'is_staff', 'created_at', 'updated_at']


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class PasswordResetRequestSerializer(serializers.ModelSerializer):
    """Serializer for password reset requests"""
    
    class Meta:
        model = PasswordResetRequest
        fields = ['id', 'user', 'reset_token', 'expires_at', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserActivitySerializer(serializers.ModelSerializer):
    """Serializer for user activity logs"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserActivity
        fields = ['id', 'user', 'username', 'activity', 'ip_address', 'user_agent', 'created_at']
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for user notifications"""
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Detailed user profile serializer"""
    
    notifications_count = serializers.SerializerMethodField()
    unread_notifications_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'mobile', 'name', 'role',
            'email_verified', 'mobile_verified', 'is_active',
            'last_login', 'created_at', 'updated_at',
            'notifications_count', 'unread_notifications_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']
    
    def get_notifications_count(self, obj):
        return obj.notifications.count()
    
    def get_unread_notifications_count(self, obj):
        return obj.notifications.filter(is_read=False).count()


class QuerySerializer(serializers.ModelSerializer):
    """Serializer for user queries/contact form submissions"""
    
    class Meta:
        model = Query
        fields = ['id', 'username', 'email', 'mobile', 'query', 'is_resolved', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_resolved', 'created_at', 'updated_at']
    
    def validate_mobile(self, value):
        """Validate mobile number"""
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("Please enter a valid mobile number (minimum 10 digits)")
        return value
    
    def validate_query(self, value):
        """Validate query is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Query cannot be empty")
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide more details (minimum 10 characters)")
        return value.strip()


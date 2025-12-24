from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT token serializer for our User model"""
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        
        return token
    
    def validate(self, attrs):
        # Get username/email and password
        username_or_email = attrs.get('username')
        password = attrs.get('password')
        
        # Authenticate user - try username first, then email
        user = None
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                from rest_framework.exceptions import AuthenticationFailed
                raise AuthenticationFailed('Invalid credentials')
        
        # Check password
        if not user.check_password(password):
            from rest_framework.exceptions import AuthenticationFailed
            raise AuthenticationFailed('Invalid credentials')
        
        # Get tokens
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

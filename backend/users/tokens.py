from rest_framework_simplejwt.tokens import RefreshToken as BaseRefreshToken
from .models import User


class RefreshToken(BaseRefreshToken):
    """Custom RefreshToken that works with users.User model"""
    
    @classmethod
    def for_user(cls, user):
        """
        Generate tokens for users.User model
        Override to add custom claims
        """
        token = cls()
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        
        return token

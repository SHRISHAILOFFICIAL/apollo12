from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class User(models.Model):
    """User model for authentication and profile management"""
    
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.CharField(max_length=150, unique=True, db_index=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    
    email_verified = models.BooleanField(default=False)
    mobile_verified = models.BooleanField(default=False)
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    last_login = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Required for Django's auth system
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']
    
    # Required properties for Django auth
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
    
    def set_password(self, raw_password):
        """Hash and set password"""
        self.password_hash = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Verify password"""
        return check_password(raw_password, self.password_hash)
    
    def __str__(self):
        return f"{self.username} ({self.role})"


class PasswordResetRequest(models.Model):
    """Track password reset requests"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets', db_index=True)
    reset_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'password_reset_requests'
    
    def __str__(self):
        return f"Reset request for {self.user.username}"


class UserActivity(models.Model):
    """Log user activities"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities', db_index=True)
    activity = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activity'
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.user.username} - {self.activity}"


class Notification(models.Model):
    """User notifications"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', db_index=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

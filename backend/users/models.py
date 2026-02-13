from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class UserManager(models.Manager):
    """Custom manager for User model - required for createsuperuser"""
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        # Create profile if it doesn't exist
        Profile = self.model._meta.apps.get_model('users', 'Profile')
        Profile.objects.get_or_create(user=user)
        return user


class User(models.Model):
    """User model for authentication and profile management"""
    
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.CharField(max_length=150, unique=True, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    
    email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text="Admin/staff access")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    # Required for Django's auth system
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    # Required properties for Django auth
    @property
    def is_anonymous(self):
        return False
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        """Required for authentication backend"""
        return True
    
    @property
    def is_superuser(self):
        """Required for admin access"""
        return self.is_staff  # Superuser if staff
    
    # JWT expects 'password' field, so we create a property
    @property
    def password(self):
        """Return password_hash as password for JWT compatibility"""
        return self.password_hash
    
    @password.setter
    def password(self, value):
        """Set password_hash when password is set"""
        self.password_hash = value
    
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
    
    def has_perm(self, perm, obj=None):
        """Required for Django admin"""
        return True
    
    def has_module_perms(self, app_label):
        """Required for Django admin"""
        return True
    
    @property
    def current_tier(self):
        """Compute current tier from active subscriptions (single source of truth)"""
        from django.utils import timezone
        
        # Avoid circular import
        from payments.models import Subscription
        
        # Check for active subscription
        active_sub = Subscription.objects.filter(
            user=self,
            status='active',
            end_date__gt=timezone.now()
        ).exists()
        
        return 'PRO' if active_sub else 'FREE'
    
    def is_pro(self):
        """Check if user has PRO tier"""
        return self.current_tier == 'PRO'
    
    def has_tier_access(self, required_tier):
        """Check if user's tier meets the required tier"""
        tier_hierarchy = {'FREE': 0, 'PRO': 1}
        user_level = tier_hierarchy.get(self.current_tier, 0)
        required_level = tier_hierarchy.get(required_tier, 0)
        return user_level >= required_level
    
    def __str__(self):
        return self.username


class Profile(models.Model):
    """User profile - simplified, subscription data moved to Subscription model"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_index=True)
    # Future: Add profile-specific fields like avatar, bio, preferences, etc.
    
    class Meta:
        db_table = 'profiles'
    
    def __str__(self):
        return f"{self.user.username} - {self.user.current_tier}"


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


class EmailOTP(models.Model):
    """Email OTP verification codes for signup and password reset"""
    
    email = models.EmailField(db_index=True)
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=[
        ('signup', 'Signup Verification'),
        ('password_reset', 'Password Reset'),
    ], default='signup')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'email_otps'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'created_at']),
            models.Index(fields=['email', 'purpose', 'is_verified']),
        ]
    
    def is_valid(self):
        """Check if OTP is still valid (10 minutes expiration)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.is_verified:
            return False
        
        expiry_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiry_time
    
    def __str__(self):
        return f"OTP for {self.email} - {self.purpose}"


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


class Query(models.Model):
    """User queries/contact form submissions"""
    
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    mobile = models.CharField(max_length=20)
    query = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'queries'
        ordering = ['-created_at']
        verbose_name_plural = 'Queries'
    
    def __str__(self):
        return f"Query from {self.username} - {self.email}"

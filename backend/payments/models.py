from django.db import models
from django.conf import settings

# Create your models here.


class Plan(models.Model):
    """Subscription plans for users"""
    
    key = models.CharField(max_length=50, unique=True, db_index=True)  # e.g., "pro_yearly"
    name = models.CharField(max_length=100)  # e.g., "PRO Plan"
    price_in_paisa = models.IntegerField(help_text="Price in paisa (1 rupee = 100 paisa)")
    duration_days = models.IntegerField(help_text="Subscription duration in days")
    features = models.JSONField(
        default=list,
        blank=True,
        help_text="List of features included in this plan"
    )
    is_active = models.BooleanField(default=True, db_index=True, help_text="Whether this plan is available for purchase")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'plans'
        ordering = ['price_in_paisa']
    
    def __str__(self):
        return f"{self.name} - ₹{self.price_in_paisa / 100}"


class Payment(models.Model):
    """Payment transactions"""
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('activated', 'Activated'),  # Payment verified and subscription activated
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', db_index=True)
    provider = models.CharField(max_length=50, default='razorpay')  # e.g., "razorpay"
    provider_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True, db_index=True)
    order_id = models.CharField(max_length=255)
    amount = models.IntegerField(help_text="Amount in paisa")
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['provider_payment_id']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.provider_payment_id} - {self.status}"


class Subscription(models.Model):
    """User subscriptions with plan tracking"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions', db_index=True)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscription')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=False)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['end_date']),
            models.Index(fields=['status', 'end_date']),
        ]
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        from django.utils import timezone
        return self.status == 'active' and self.end_date > timezone.now()
    
    @property
    def days_remaining(self):
        """Calculate days remaining in subscription"""
        from django.utils import timezone
        if self.end_date > timezone.now():
            delta = self.end_date - timezone.now()
            return delta.days
        return 0
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"

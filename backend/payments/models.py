from django.db import models
from django.conf import settings

# Create your models here.


class Plan(models.Model):
    """Subscription plans for users"""
    
    key = models.CharField(max_length=50, unique=True, db_index=True)  # e.g., "monthly", "yearly"
    name = models.CharField(max_length=100)
    price_in_paisa = models.IntegerField(help_text="Price in paisa (1 rupee = 100 paisa)")
    duration_days = models.IntegerField(help_text="Subscription duration in days")
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
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', db_index=True)
    provider = models.CharField(max_length=50, default='razorpay')  # e.g., "razorpay"
    provider_payment_id = models.CharField(max_length=255, unique=True, db_index=True)
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

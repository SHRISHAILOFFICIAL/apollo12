"""
Serializers for payment-related models
"""
from rest_framework import serializers
from .models import Plan, Payment


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for subscription plans"""
    
    price_in_rupees = serializers.SerializerMethodField()
    
    class Meta:
        model = Plan
        fields = ['id', 'key', 'name', 'price_in_paisa', 'price_in_rupees', 
                  'duration_days', 'features', 'is_active']
    
    def get_price_in_rupees(self, obj):
        """Convert paisa to rupees for display"""
        return obj.price_in_paisa / 100


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment transactions"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    amount_in_rupees = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = ['id', 'username', 'provider', 'provider_payment_id', 'order_id',
                  'amount', 'amount_in_rupees', 'currency', 'status', 'metadata',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_amount_in_rupees(self, obj):
        """Convert paisa to rupees for display"""
        return obj.amount / 100


class CreateOrderSerializer(serializers.Serializer):
    """Serializer for creating a Razorpay order"""
    
    plan_id = serializers.IntegerField(required=True)
    
    def validate_plan_id(self, value):
        """Validate that the plan exists and is active"""
        try:
            plan = Plan.objects.get(id=value, is_active=True)
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive plan")
        return value


class VerifyPaymentSerializer(serializers.Serializer):
    """Serializer for verifying payment"""
    
    razorpay_order_id = serializers.CharField(required=True)
    razorpay_payment_id = serializers.CharField(required=True)
    razorpay_signature = serializers.CharField(required=True)
    plan_id = serializers.IntegerField(required=True)
    
    def validate_plan_id(self, value):
        """Validate that the plan exists"""
        try:
            plan = Plan.objects.get(id=value)
        except Plan.DoesNotExist:
            raise serializers.ValidationError("Invalid plan")
        return value

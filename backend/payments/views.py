"""
Payment API views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Plan, Payment
from .serializers import (
    PlanSerializer, 
    PaymentSerializer, 
    CreateOrderSerializer, 
    VerifyPaymentSerializer
)
from .razorpay_client import razorpay_client
from users.models import User

logger = logging.getLogger(__name__)


@api_view(['GET'])
def list_plans(request):
    """
    List all active subscription plans
    
    GET /api/payments/plans/
    """
    plans = Plan.objects.filter(is_active=True)
    serializer = PlanSerializer(plans, many=True)
    return Response({
        'success': True,
        'plans': serializer.data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create a Razorpay order for a plan
    
    POST /api/payments/create-order/
    Body: { "plan_id": 1 }
    """
    serializer = CreateOrderSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        plan = Plan.objects.get(id=serializer.validated_data['plan_id'], is_active=True)
        
        # Create Razorpay order
        receipt = f"order_{request.user.id}_{timezone.now().timestamp()}"
        notes = {
            'user_id': request.user.id,
            'username': request.user.username,
            'plan_id': plan.id,
            'plan_name': plan.name
        }
        
        razorpay_order = razorpay_client.create_order(
            amount_in_paisa=plan.price_in_paisa,
            receipt=receipt,
            notes=notes
        )
        
        # Create payment record in database
        payment = Payment.objects.create(
            user=request.user,
            provider='razorpay',
            provider_payment_id='',  # Will be updated after payment
            order_id=razorpay_order['id'],
            amount=plan.price_in_paisa,
            currency='INR',
            status='created',
            metadata={
                'plan_id': plan.id,
                'plan_name': plan.name,
                'receipt': receipt
            }
        )
        
        logger.info(f"Order created for user {request.user.username}: {razorpay_order['id']}")
        
        return Response({
            'success': True,
            'order': {
                'id': razorpay_order['id'],
                'amount': razorpay_order['amount'],
                'currency': razorpay_order['currency'],
                'receipt': receipt
            },
            'plan': PlanSerializer(plan).data,
            'razorpay_key_id': razorpay_client.client.auth[0]  # Public key for frontend
        })
    
    except Plan.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Plan not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Failed to create order: {str(e)}")
        return Response({
            'success': False,
            'error': 'Failed to create order'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    """
    Verify payment and activate subscription
    
    POST /api/payments/verify-payment/
    Body: {
        "razorpay_order_id": "order_xxx",
        "razorpay_payment_id": "pay_xxx",
        "razorpay_signature": "signature_xxx",
        "plan_id": 1
    }
    """
    serializer = VerifyPaymentSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response({
            'success': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        data = serializer.validated_data
        
        # Verify payment signature
        is_valid = razorpay_client.verify_payment_signature(
            razorpay_order_id=data['razorpay_order_id'],
            razorpay_payment_id=data['razorpay_payment_id'],
            razorpay_signature=data['razorpay_signature']
        )
        
        if not is_valid:
            return Response({
                'success': False,
                'error': 'Invalid payment signature'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get plan
        plan = Plan.objects.get(id=data['plan_id'])
        
        # Update payment record
        payment = Payment.objects.get(
            order_id=data['razorpay_order_id'],
            user=request.user
        )
        payment.provider_payment_id = data['razorpay_payment_id']
        payment.status = 'paid'
        payment.metadata['verified_at'] = timezone.now().isoformat()
        payment.save()
        
        # Upgrade user to PRO tier
        user = request.user
        user.user_tier = 'PRO'
        user.save()
        
        # Update user profile
        profile = user.profile
        profile.is_paid = True
        profile.plan = plan
        profile.subscription_start = timezone.now()
        profile.subscription_end = timezone.now() + timedelta(days=plan.duration_days)
        profile.save()
        
        logger.info(f"Payment verified and user {user.username} upgraded to PRO")
        
        return Response({
            'success': True,
            'message': 'Payment verified successfully! You are now a PRO user.',
            'user': {
                'tier': user.user_tier,
                'subscription_end': profile.subscription_end.isoformat()
            }
        })
    
    except Payment.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Payment record not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    except Exception as e:
        logger.error(f"Failed to verify payment: {str(e)}")
        return Response({
            'success': False,
            'error': 'Failed to verify payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    """
    Get user's payment history
    
    GET /api/payments/history/
    """
    payments = Payment.objects.filter(user=request.user).order_by('-created_at')
    serializer = PaymentSerializer(payments, many=True)
    
    return Response({
        'success': True,
        'payments': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    """
    Get current subscription status
    
    GET /api/payments/subscription-status/
    """
    user = request.user
    profile = user.profile
    
    return Response({
        'success': True,
        'subscription': {
            'tier': user.user_tier,
            'is_pro': user.is_pro(),
            'is_paid': profile.is_paid,
            'plan': PlanSerializer(profile.plan).data if profile.plan else None,
            'subscription_start': profile.subscription_start,
            'subscription_end': profile.subscription_end,
            'is_active': profile.is_subscription_active
        }
    })

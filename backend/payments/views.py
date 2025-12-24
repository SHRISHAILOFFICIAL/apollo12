"""
Payment API views
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from datetime import timedelta
import logging
import json

from .models import Plan, Payment
from .serializers import (
    PlanSerializer, 
    PaymentSerializer, 
    CreateOrderSerializer, 
    VerifyPaymentSerializer
)
from .razorpay_client import razorpay_client
from .webhook_handler import WebhookHandler
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
            provider_payment_id=None,  # Will be updated after payment (NULL to avoid unique constraint)
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
        payment.metadata['verification_method'] = 'manual'
        payment.save()
        
        # Create Subscription record (single source of truth for tier)
        from .models import Subscription
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            payment=payment,
            status='active',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=plan.duration_days),
            auto_renew=False
        )
        
        # Update payment status to activated
        payment.status = 'activated'
        payment.save()
        
        logger.info(f"Payment verified and user {request.user.username} upgraded to PRO (Subscription ID: {subscription.id})")
        
        return Response({
            'success': True,
            'message': 'Payment verified successfully! You are now a PRO user.',
            'user': {
                'tier': request.user.current_tier,
                'subscription_end': subscription.end_date.isoformat()
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
    from .models import Subscription
    user = request.user
    
    # Get active subscription
    active_sub = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gt=timezone.now()
    ).select_related('plan').first()
    
    return Response({
        'success': True,
        'subscription': {
            'tier': user.current_tier,
            'is_pro': user.is_pro(),
            'plan': PlanSerializer(active_sub.plan).data if active_sub else None,
            'subscription_start': active_sub.start_date if active_sub else None,
            'subscription_end': active_sub.end_date if active_sub else None,
            'is_active': active_sub.is_active if active_sub else False,
            'days_remaining': active_sub.days_remaining if active_sub else 0
        }
    })


@csrf_exempt
@api_view(['POST'])
def razorpay_webhook(request):
    """
    Handle Razorpay webhook events
    
    POST /api/payments/webhook/razorpay/
    
    Events handled:
    - payment.captured: Payment successful
    - payment.failed: Payment failed
    - refund.created: Refund initiated
    """
    try:
        # Get webhook signature from headers
        webhook_signature = request.META.get('HTTP_X_RAZORPAY_SIGNATURE')
        webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        
        if not webhook_signature:
            logger.error("Webhook signature missing")
            return HttpResponse('Signature missing', status=400)
        
        if not webhook_secret:
            logger.error("Webhook secret not configured")
            return HttpResponse('Webhook not configured', status=500)
        
        # Get raw payload
        payload = request.body
        
        # Verify signature
        is_valid = WebhookHandler.verify_signature(
            payload=payload,
            signature=webhook_signature,
            secret=webhook_secret
        )
        
        if not is_valid:
            logger.error("Invalid webhook signature")
            return HttpResponse('Invalid signature', status=400)
        
        # Parse event data
        event_data = json.loads(payload)
        event_type = event_data.get('event')
        
        logger.info(f"Received webhook event: {event_type}")
        
        # Process webhook
        success, message = WebhookHandler.process_webhook(event_type, event_data)
        
        if success:
            logger.info(f"Webhook processed successfully: {event_type}")
            return HttpResponse('OK', status=200)
        else:
            logger.error(f"Webhook processing failed: {message}")
            return HttpResponse(f'Processing failed: {message}', status=400)
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in webhook payload")
        return HttpResponse('Invalid JSON', status=400)
    
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}", exc_info=True)
        return HttpResponse('Internal error', status=500)

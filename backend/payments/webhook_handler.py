"""
Razorpay webhook handler for payment events
Handles payment success, failure, and refund events with idempotency
"""
import hmac
import hashlib
import logging
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from .models import Payment, Plan
from users.models import User

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handle Razorpay webhook events"""
    
    @staticmethod
    def verify_signature(payload, signature, secret):
        """
        Verify Razorpay webhook signature
        
        Args:
            payload (bytes): Raw webhook payload
            signature (str): X-Razorpay-Signature header value
            secret (str): Webhook secret from settings
        
        Returns:
            bool: True if signature is valid
        """
        try:
            expected_signature = hmac.new(
                secret.encode('utf-8'),
                payload,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
        except Exception as e:
            logger.error(f"Signature verification error: {str(e)}")
            return False
    
    @staticmethod
    @transaction.atomic
    def handle_payment_captured(event_data):
        """
        Handle payment.captured event
        
        Args:
            event_data (dict): Payment event data from Razorpay
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            payment_entity = event_data.get('payload', {}).get('payment', {}).get('entity', {})
            
            razorpay_payment_id = payment_entity.get('id')
            razorpay_order_id = payment_entity.get('order_id')
            amount = payment_entity.get('amount')
            status = payment_entity.get('status')
            
            if not all([razorpay_payment_id, razorpay_order_id]):
                logger.error("Missing required payment fields in webhook")
                return False, "Missing required fields"
            
            # Check for existing payment (idempotency)
            existing_payment = Payment.objects.filter(
                provider_payment_id=razorpay_payment_id
            ).first()
            
            if existing_payment and existing_payment.status == 'paid':
                logger.info(f"Payment {razorpay_payment_id} already processed (idempotent)")
                return True, "Already processed"
            
            # Get payment record by order_id
            payment = Payment.objects.filter(order_id=razorpay_order_id).first()
            
            if not payment:
                logger.error(f"Payment record not found for order {razorpay_order_id}")
                return False, "Payment record not found"
            
            # Update payment record
            payment.provider_payment_id = razorpay_payment_id
            payment.status = 'paid'
            payment.metadata['webhook_received_at'] = timezone.now().isoformat()
            payment.metadata['razorpay_status'] = status
            payment.save()
            
            # Activate subscription
            user = payment.user
            plan_id = payment.metadata.get('plan_id')
            
            if plan_id:
                plan = Plan.objects.get(id=plan_id)
                
                # Create Subscription record (single source of truth)
                from .models import Subscription
                subscription = Subscription.objects.create(
                    user=user,
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
                
                logger.info(f"Subscription activated for user {user.username} via webhook (Subscription ID: {subscription.id})")
            
            return True, "Payment processed successfully"
        
        except Exception as e:
            logger.error(f"Error handling payment.captured: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    @transaction.atomic
    def handle_payment_failed(event_data):
        """
        Handle payment.failed event
        
        Args:
            event_data (dict): Payment event data from Razorpay
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            payment_entity = event_data.get('payload', {}).get('payment', {}).get('entity', {})
            
            razorpay_payment_id = payment_entity.get('id')
            razorpay_order_id = payment_entity.get('order_id')
            error_code = payment_entity.get('error_code')
            error_description = payment_entity.get('error_description')
            
            # Get payment record
            payment = Payment.objects.filter(order_id=razorpay_order_id).first()
            
            if not payment:
                logger.error(f"Payment record not found for order {razorpay_order_id}")
                return False, "Payment record not found"
            
            # Update payment status
            payment.provider_payment_id = razorpay_payment_id or ''
            payment.status = 'failed'
            payment.metadata['webhook_received_at'] = timezone.now().isoformat()
            payment.metadata['error_code'] = error_code
            payment.metadata['error_description'] = error_description
            payment.save()
            
            logger.warning(f"Payment failed for order {razorpay_order_id}: {error_description}")
            
            return True, "Payment failure recorded"
        
        except Exception as e:
            logger.error(f"Error handling payment.failed: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    @transaction.atomic
    def handle_refund_created(event_data):
        """
        Handle refund.created event
        
        Args:
            event_data (dict): Refund event data from Razorpay
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            refund_entity = event_data.get('payload', {}).get('refund', {}).get('entity', {})
            
            razorpay_payment_id = refund_entity.get('payment_id')
            refund_id = refund_entity.get('id')
            amount = refund_entity.get('amount')
            
            # Get payment record
            payment = Payment.objects.filter(provider_payment_id=razorpay_payment_id).first()
            
            if not payment:
                logger.error(f"Payment not found for refund {refund_id}")
                return False, "Payment not found"
            
            # Update payment status
            payment.status = 'refunded'
            payment.metadata['refund_id'] = refund_id
            payment.metadata['refund_amount'] = amount
            payment.metadata['refunded_at'] = timezone.now().isoformat()
            payment.save()
            
            # Cancel subscription if this was their active subscription
            user = payment.user
            
            # Find and cancel the subscription associated with this payment
            from .models import Subscription
            subscription = Subscription.objects.filter(
                user=user,
                payment=payment,
                status='active'
            ).first()
            
            if subscription:
                subscription.status = 'cancelled'
                subscription.cancelled_at = timezone.now()
                subscription.save()
                
                logger.info(f"Subscription cancelled for user {user.username} due to refund")
            
            return True, "Refund processed successfully"
        
        except Exception as e:
            logger.error(f"Error handling refund.created: {str(e)}", exc_info=True)
            return False, str(e)
    
    @staticmethod
    def process_webhook(event_type, event_data):
        """
        Process webhook based on event type
        
        Args:
            event_type (str): Type of webhook event
            event_data (dict): Event data
        
        Returns:
            tuple: (success: bool, message: str)
        """
        handlers = {
            'payment.captured': WebhookHandler.handle_payment_captured,
            'payment.failed': WebhookHandler.handle_payment_failed,
            'refund.created': WebhookHandler.handle_refund_created,
        }
        
        handler = handlers.get(event_type)
        
        if not handler:
            logger.warning(f"Unhandled webhook event type: {event_type}")
            return False, f"Unhandled event type: {event_type}"
        
        return handler(event_data)

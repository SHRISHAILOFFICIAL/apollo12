"""
Razorpay client wrapper for payment processing
"""
import razorpay
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class RazorpayClient:
    """Wrapper for Razorpay API client"""
    
    def __init__(self):
        """Initialize Razorpay client with API credentials"""
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        self.client.set_app_details({
            "title": "DCET Platform",
            "version": "1.0.0"
        })
    
    def create_order(self, amount_in_paisa, currency='INR', receipt=None, notes=None):
        """
        Create a Razorpay order
        
        Args:
            amount_in_paisa (int): Amount in paisa (1 rupee = 100 paisa)
            currency (str): Currency code (default: INR)
            receipt (str): Receipt ID for reference
            notes (dict): Additional notes/metadata
        
        Returns:
            dict: Order details from Razorpay
        """
        try:
            order_data = {
                'amount': amount_in_paisa,
                'currency': currency,
                'payment_capture': 1  # Auto-capture payment
            }
            
            if receipt:
                order_data['receipt'] = receipt
            
            if notes:
                order_data['notes'] = notes
            
            order = self.client.order.create(data=order_data)
            logger.info(f"Razorpay order created: {order['id']}")
            return order
        
        except Exception as e:
            logger.error(f"Failed to create Razorpay order: {str(e)}")
            raise
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """
        Verify payment signature to ensure payment authenticity
        
        Args:
            razorpay_order_id (str): Order ID from Razorpay
            razorpay_payment_id (str): Payment ID from Razorpay
            razorpay_signature (str): Signature from Razorpay
        
        Returns:
            bool: True if signature is valid, False otherwise
        """
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            # This will raise SignatureVerificationError if invalid
            self.client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment signature verified for order: {razorpay_order_id}")
            return True
        
        except razorpay.errors.SignatureVerificationError as e:
            logger.error(f"Payment signature verification failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error verifying payment signature: {str(e)}")
            return False
    
    def fetch_payment(self, payment_id):
        """
        Fetch payment details from Razorpay
        
        Args:
            payment_id (str): Payment ID from Razorpay
        
        Returns:
            dict: Payment details
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            logger.error(f"Failed to fetch payment {payment_id}: {str(e)}")
            raise
    
    def fetch_order(self, order_id):
        """
        Fetch order details from Razorpay
        
        Args:
            order_id (str): Order ID from Razorpay
        
        Returns:
            dict: Order details
        """
        try:
            order = self.client.order.fetch(order_id)
            return order
        except Exception as e:
            logger.error(f"Failed to fetch order {order_id}: {str(e)}")
            raise


# Singleton instance
razorpay_client = RazorpayClient()

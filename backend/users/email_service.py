"""
Email service for sending OTP verification emails via Brevo
"""
import random
from django.core.mail import send_mail
from django.conf import settings


def generate_otp():
    """Generate a 6-digit OTP code"""
    return str(random.randint(100000, 999999))


def send_otp_email(email, otp, purpose='signup'):
    """
    Send OTP verification email via Brevo
    
    Args:
        email (str): Recipient email address
        otp (str): 6-digit OTP code
        purpose (str): 'signup' or 'password_reset'
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    if purpose == 'signup':
        subject = 'Verify Your Email - Apollo11 DCET Platform'
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4CAF50;">Welcome to Apollo11!</h2>
                    <p>Thank you for signing up for the DCET Mock Test Platform.</p>
                    <p>Your email verification code is:</p>
                    <div style="background-color: #f4f4f4; padding: 15px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #4CAF50; margin: 0; font-size: 36px; letter-spacing: 5px;">{otp}</h1>
                    </div>
                    <p><strong>This code will expire in 10 minutes.</strong></p>
                    <p>If you didn't request this verification code, please ignore this email.</p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    <p style="color: #666; font-size: 12px;">
                        Apollo11 DCET Mock Test Platform<br>
                        Preparing you for success in DCET exams
                    </p>
                </div>
            </body>
        </html>
        """
        plain_message = f"""
        Welcome to Apollo11!
        
        Thank you for signing up for the DCET Mock Test Platform.
        
        Your email verification code is: {otp}
        
        This code will expire in 10 minutes.
        
        If you didn't request this verification code, please ignore this email.
        
        ---
        Apollo11 DCET Mock Test Platform
        Preparing you for success in DCET exams
        """
    else:  # password_reset
        subject = 'Password Reset Code - Apollo11 DCET Platform'
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #FF5722;">Password Reset Request</h2>
                    <p>We received a request to reset your password for Apollo11 DCET Platform.</p>
                    <p>Your password reset code is:</p>
                    <div style="background-color: #f4f4f4; padding: 15px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #FF5722; margin: 0; font-size: 36px; letter-spacing: 5px;">{otp}</h1>
                    </div>
                    <p><strong>This code will expire in 10 minutes.</strong></p>
                    <p>If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 30px 0;">
                    <p style="color: #666; font-size: 12px;">
                        Apollo11 DCET Mock Test Platform<br>
                        Preparing you for success in DCET exams
                    </p>
                </div>
            </body>
        </html>
        """
        plain_message = f"""
        Password Reset Request
        
        We received a request to reset your password for Apollo11 DCET Platform.
        
        Your password reset code is: {otp}
        
        This code will expire in 10 minutes.
        
        If you didn't request a password reset, please ignore this email and your password will remain unchanged.
        
        ---
        Apollo11 DCET Mock Test Platform
        Preparing you for success in DCET exams
        """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email to {email}: {str(e)}")
        return False

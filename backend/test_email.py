"""
Quick Email Test Script
Run this to verify your Brevo email configuration is working
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.email_service import send_otp_email, generate_otp

def test_email():
    print("=" * 60)
    print("Apollo11 Email Configuration Test")
    print("=" * 60)
    print()
    
    # Get email from user
    email = input("Enter your email address to test: ").strip()
    
    if not email:
        print("❌ Email address is required!")
        return
    
    # Generate OTP
    otp = generate_otp()
    print(f"\n📧 Sending test email to: {email}")
    print(f"🔢 OTP Code: {otp}")
    print()
    
    # Test signup email
    print("Testing Signup OTP Email...")
    result_signup = send_otp_email(email, otp, purpose='signup')
    
    if result_signup:
        print("✅ Signup email sent successfully!")
    else:
        print("❌ Failed to send signup email")
        print("\nPossible issues:")
        print("1. Check if BREVO_API_KEY is set in .env file")
        print("2. Verify sender email in Brevo dashboard")
        print("3. Check if django-anymail[brevo] is installed")
        return
    
    print()
    
    # Test password reset email
    print("Testing Password Reset OTP Email...")
    result_reset = send_otp_email(email, otp, purpose='password_reset')
    
    if result_reset:
        print("✅ Password reset email sent successfully!")
    else:
        print("❌ Failed to send password reset email")
        return
    
    print()
    print("=" * 60)
    print("✅ All tests passed! Check your inbox.")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Check your email inbox")
    print("2. Verify the emails look good")
    print("3. Your email service is ready to use!")

if __name__ == '__main__':
    try:
        test_email()
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set BREVO_API_KEY in .env file")
        print("2. Installed django-anymail: pip install django-anymail[brevo]")
        print("3. Verified sender email in Brevo dashboard")

"""
Environment Configuration Verification Script
Checks if all environment variables are loaded correctly
"""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_path))

# Load Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

try:
    import django
    django.setup()
    from django.conf import settings
except Exception as e:
    print(f"❌ Error loading Django: {e}")
    sys.exit(1)

def check_config():
    print("=" * 70)
    print("Apollo11 Environment Configuration Check")
    print("=" * 70)
    print()
    
    checks = []
    
    # Check SECRET_KEY
    secret_key = settings.SECRET_KEY
    if secret_key and len(secret_key) > 20:
        checks.append(("✅", "SECRET_KEY", "Loaded successfully"))
    else:
        checks.append(("❌", "SECRET_KEY", "Not set or too short"))
    
    # Check DEBUG
    debug = settings.DEBUG
    checks.append(("✅" if debug else "⚠️", "DEBUG", f"Set to {debug}"))
    
    # Check Database
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    checks.append(("✅", "DATABASE", f"{db_name} (user: {db_user})"))
    
    # Check Redis
    redis_location = settings.CACHES['default']['LOCATION']
    checks.append(("✅", "REDIS", redis_location))
    
    # Check Email (Brevo)
    brevo_key = settings.ANYMAIL.get('BREVO_API_KEY', '')
    if brevo_key and len(brevo_key) > 20:
        # Show only first 20 chars for security
        key_preview = brevo_key[:20] + "..." + brevo_key[-10:]
        checks.append(("✅", "BREVO_API_KEY", f"{key_preview}"))
    else:
        checks.append(("❌", "BREVO_API_KEY", "Not set or invalid"))
    
    # Check FROM_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL
    if from_email and '@' in from_email:
        checks.append(("✅", "DEFAULT_FROM_EMAIL", from_email))
    else:
        checks.append(("❌", "DEFAULT_FROM_EMAIL", "Not set or invalid"))
    
    # Check CORS
    cors_origins = settings.CORS_ALLOWED_ORIGINS
    checks.append(("✅", "CORS_ALLOWED_ORIGINS", str(cors_origins)))
    
    # Print results
    print("Configuration Status:")
    print("-" * 70)
    for status, key, value in checks:
        print(f"{status} {key:25s} : {value}")
    
    print()
    print("=" * 70)
    
    # Summary
    success_count = sum(1 for c in checks if c[0] == "✅")
    total_count = len(checks)
    
    if success_count == total_count:
        print(f"✅ All {total_count} checks passed! Configuration is correct.")
    else:
        print(f"⚠️  {success_count}/{total_count} checks passed.")
        print()
        print("Issues found:")
        for status, key, value in checks:
            if status == "❌":
                print(f"  - {key}: {value}")
        print()
        print("Please check your .env file and ensure all values are set correctly.")
    
    print("=" * 70)
    print()
    
    # Test email import
    print("Testing email service import...")
    try:
        from users.email_service import send_otp_email, generate_otp
        print("✅ Email service imported successfully")
        print()
        print("You can now test email sending with:")
        print("  python test_email.py")
    except Exception as e:
        print(f"❌ Error importing email service: {e}")
    
    print()

if __name__ == '__main__':
    try:
        check_config()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

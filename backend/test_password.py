"""
Test script to verify password hashing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

# Get the demo4 user
try:
    user = User.objects.get(username='demo4')
    print(f"User found: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password hash (first 50 chars): {user.password_hash[:50]}")
    print(f"Password hash starts with 'pbkdf2': {user.password_hash.startswith('pbkdf2')}")
    
    # Test password checking
    test_password = input("\nEnter the password you used during registration: ")
    is_correct = user.check_password(test_password)
    print(f"\nPassword check result: {is_correct}")
    
    if is_correct:
        print("✅ Password is correct! Login should work.")
    else:
        print("❌ Password is incorrect. This is why login is failing.")
        print("\nLet me reset the password for you...")
        new_password = input("Enter a new password: ")
        user.set_password(new_password)
        user.save()
        print(f"✅ Password updated! New hash: {user.password_hash[:50]}")
        print("Try logging in with the new password.")
        
except User.DoesNotExist:
    print("User 'demo4' not found in database")

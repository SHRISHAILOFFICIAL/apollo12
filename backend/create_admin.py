"""
Script to create an admin user for accessing admin analytics endpoints
Run with: python manage.py shell < create_admin.py
"""
import django
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User

def create_admin():
    """Create admin user with staff access"""
    
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        print("❌ Admin user already exists!")
        admin = User.objects.get(username='admin')
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Is Staff: {admin.is_staff}")
        
        # Update to staff if not already
        if not admin.is_staff:
            admin.is_staff = True
            admin.save()
            print("✅ Updated existing admin to staff")
        return
    
    # Create new admin user
    admin = User.objects.create(
        username='admin',
        email='admin@apollo11.com',
        email_verified=True,
        is_staff=True  # Enable admin access
    )
    admin.set_password('admin123')  # Change this in production!
    admin.save()
    
    print("✅ Admin user created successfully!")
    print(f"Username: admin")
    print(f"Password: admin123")
    print(f"Email: {admin.email}")
    print(f"Is Staff: {admin.is_staff}")
    print("\n🔗 Access Django Admin at: http://localhost:8000/admin/")
    print("⚠️  IMPORTANT: Change the password after first login!")

if __name__ == '__main__':
    create_admin()

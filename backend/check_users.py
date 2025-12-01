import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import User

print("Checking users...")
users = User.objects.all()
print(f"Total users: {users.count()}")

for u in users:
    print(f"\nUsername: {u.username}")
    print(f"Email: {u.email}")
    print(f"Is active: {u.is_active}")
    print(f"Is staff: {u.is_staff}")
    
student = User.objects.filter(username='student').first()
if student:
    print(f"\n✅ Student user found!")
    print(f"Password check with 'student123': {student.check_password('student123')}")
else:
    print("❌ Student user not found!")

"""
Reset database and migrations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
import shutil

print("="*60)
print("  DATABASE RESET SCRIPT")
print("="*60)

# Step 1: Delete all migration files except __init__.py
print("\n1. Deleting migration files...")
apps = ['users', 'exams', 'results', 'payments', 'analytics', 'adminpanel', 'core']

for app in apps:
    migrations_dir = f'd:\\quiz\\backend\\{app}\\migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                file_path = os.path.join(migrations_dir, file)
                os.remove(file_path)
                print(f"   Deleted: {app}/migrations/{file}")

print("\n2. Please manually drop and recreate the database:")
print("   Run in MySQL:")
print("   DROP DATABASE IF EXISTS dcet_platform;")
print("   CREATE DATABASE dcet_platform;")
print("\n   Then press Enter to continue...")
input()

# Step 3: Create new migrations
print("\n3. Creating fresh migrations...")
call_command('makemigrations')

# Step 4: Apply migrations
print("\n4. Applying migrations...")
call_command('migrate')

print("\n5. Creating superuser...")
print("   Username: shri")
print("   Email: shrishailkone.21@gmail.com")
call_command('createsuperuser', '--username', 'shri', '--email', 'shrishailkone.21@gmail.com')

print("\n" + "="*60)
print("  Database reset complete!")
print("="*60)

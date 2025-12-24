"""
Data migration script to migrate existing Profile subscription data to new Subscription model
Run with: python manage.py shell < payments/data_migration.py
"""
import django
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from users.models import User, Profile
from payments.models import Subscription, Plan, Payment

def migrate_subscriptions():
    """Migrate existing PRO users from Profile to Subscription model"""
    
    print("Starting subscription data migration...")
    
    # Get all users with profile subscription data (old system)
    # We'll migrate any user who has subscription_end set in their profile
    profiles_with_subs = Profile.objects.filter(
        subscription_end__isnull=False
    ).select_related('user')
    
    migrated_count = 0
    skipped_count = 0
    
    for profile in profiles_with_subs:
        user = profile.user
        try:
            
            # Skip if no subscription data
            if not profile.plan or not profile.subscription_end:
                print(f"Skipping {user.username}: No subscription data")
                skipped_count += 1
                continue
            
            # Check if subscription already exists
            existing_sub = Subscription.objects.filter(user=user, status='active').first()
            if existing_sub:
                print(f"Skipping {user.username}: Subscription already exists")
                skipped_count += 1
                continue
            
            # Find associated payment (most recent paid payment)
            payment = Payment.objects.filter(
                user=user,
                status='paid'
            ).order_by('-created_at').first()
            
            # Determine status
            status = 'active' if profile.subscription_end > timezone.now() else 'expired'
            
            # Create subscription
            subscription = Subscription.objects.create(
                user=user,
                plan=profile.plan,
                payment=payment,
                status=status,
                start_date=profile.subscription_start or timezone.now(),
                end_date=profile.subscription_end,
                auto_renew=False
            )
            
            print(f"✓ Migrated {user.username}: {subscription.plan.name} ({status})")
            migrated_count += 1
            
        except Exception as e:
            print(f"✗ Error migrating {user.username}: {str(e)}")
    
    print(f"\nMigration complete!")
    print(f"Migrated: {migrated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Total PRO users: {pro_users.count()}")

if __name__ == '__main__':
    migrate_subscriptions()

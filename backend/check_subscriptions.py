import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from payments.models import Subscription, Payment
from django.utils import timezone

print("=== User Subscription Status ===\n")

users = User.objects.all()
for user in users:
    paid_payments = Payment.objects.filter(
        user=user, 
        status__in=['paid', 'activated']
    ).count()
    
    active_subs = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gt=timezone.now()
    ).count()
    
    print(f"{user.username}:")
    print(f"  Current Tier: {user.current_tier}")
    print(f"  Paid Payments: {paid_payments}")
    print(f"  Active Subscriptions: {active_subs}")
    print()

# Check for payments without subscriptions
print("\n=== Payments Without Subscriptions ===")
paid_payments = Payment.objects.filter(status__in=['paid', 'activated'])
for payment in paid_payments:
    has_sub = Subscription.objects.filter(payment=payment).exists()
    if not has_sub:
        print(f"Payment ID {payment.id} for {payment.user.username} has NO subscription!")

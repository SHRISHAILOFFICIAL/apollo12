import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.models import User
from payments.models import Subscription, Payment, Plan
from django.utils import timezone
from datetime import timedelta

print("=== Creating Subscriptions for Paid Users ===\n")

# Get all paid/activated payments without subscriptions
paid_payments = Payment.objects.filter(status__in=['paid', 'activated'])

for payment in paid_payments:
    # Check if subscription already exists
    existing_sub = Subscription.objects.filter(payment=payment).first()
    
    if existing_sub:
        print(f"✓ Payment {payment.id} for {payment.user.username} already has subscription")
        continue
    
    # Get plan from payment metadata or use default PRO plan
    plan_id = payment.metadata.get('plan_id')
    
    if plan_id:
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            print(f"! Plan {plan_id} not found, using default PRO plan")
            plan = Plan.objects.filter(key='pro').first()
    else:
        print(f"! No plan_id in metadata for payment {payment.id}, using default PRO plan")
        plan = Plan.objects.filter(key='pro').first()
    
    if not plan:
        print(f"✗ ERROR: No PRO plan found! Cannot create subscription for payment {payment.id}")
        continue
    
    # Create subscription
    start_date = payment.created_at
    end_date = start_date + timedelta(days=plan.duration_days)
    
    # Check if subscription should still be active
    status = 'active' if end_date > timezone.now() else 'expired'
    
    subscription = Subscription.objects.create(
        user=payment.user,
        plan=plan,
        payment=payment,
        status=status,
        start_date=start_date,
        end_date=end_date,
        auto_renew=False
    )
    
    print(f"✓ Created subscription for {payment.user.username}")
    print(f"  Plan: {plan.name}")
    print(f"  Status: {status}")
    print(f"  End Date: {end_date}")
    print()

print("\n=== Verification ===")
print(f"Total paid payments: {paid_payments.count()}")
print(f"Total subscriptions: {Subscription.objects.count()}")

print("\n=== User Status After Fix ===")
users = User.objects.all()
for user in users:
    print(f"{user.username}: {user.current_tier}")

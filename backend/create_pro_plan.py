"""
Script to create initial PRO plan in the database
Run this with: python manage.py shell < create_pro_plan.py
"""
from payments.models import Plan

# Create PRO plan
pro_plan, created = Plan.objects.get_or_create(
    key='pro_yearly',
    defaults={
        'name': 'PRO Plan',
        'price_in_paisa': 14900,  # ₹149
        'duration_days': 365,  # 1 year
        'features': [
            '3 Previous Year Question Papers (PYQs)',
            '10 Mock Tests',
            'Video Solutions for all important questions',
            'Detailed analytics and performance tracking',
            'Unlimited attempts on all exams',
            'Priority support'
        ],
        'is_active': True
    }
)

if created:
    print(f"✅ Created PRO plan: {pro_plan.name} - ₹{pro_plan.price_in_paisa / 100}")
else:
    print(f"ℹ️  PRO plan already exists: {pro_plan.name}")

print("\n📊 Current Plans:")
for plan in Plan.objects.all():
    print(f"  - {plan.name}: ₹{plan.price_in_paisa / 100} for {plan.duration_days} days")

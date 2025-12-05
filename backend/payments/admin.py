from django.contrib import admin
from .models import Plan, Payment

# Register your models here.


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'price_in_rupees', 'duration_days', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'key']
    
    def price_in_rupees(self, obj):
        return f"₹{obj.price_in_paisa / 100:.2f}"
    price_in_rupees.short_description = 'Price'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'provider_payment_id', 'amount_in_rupees', 'status', 'provider', 'created_at']
    list_filter = ['status', 'provider', 'created_at']
    search_fields = ['user__username', 'provider_payment_id', 'order_id']
    raw_id_fields = ['user']
    readonly_fields = ['created_at', 'updated_at']
    
    def amount_in_rupees(self, obj):
        return f"₹{obj.amount / 100:.2f}"
    amount_in_rupees.short_description = 'Amount'

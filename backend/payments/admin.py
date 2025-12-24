"""
Django admin configuration for payment models
"""
from django.contrib import admin
from .models import Plan, Payment, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'price_in_rupees', 'duration_days', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'key']
    readonly_fields = ['created_at']
    
    def price_in_rupees(self, obj):
        return f"₹{obj.price_in_paisa / 100}"
    price_in_rupees.short_description = 'Price'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount_rupees', 'status', 'provider', 'created_at']
    list_filter = ['status', 'provider', 'created_at']
    search_fields = ['user__username', 'provider_payment_id', 'order_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Info', {
            'fields': ('user', 'provider', 'provider_payment_id', 'order_id')
        }),
        ('Amount', {
            'fields': ('amount', 'currency')
        }),
        ('Status', {
            'fields': ('status', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_rupees(self, obj):
        return f"₹{obj.amount / 100}"
    amount_rupees.short_description = 'Amount'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'days_remaining', 'is_active']
    list_filter = ['status', 'plan', 'auto_renew', 'start_date']
    search_fields = ['user__username', 'plan__name']
    readonly_fields = ['created_at', 'updated_at', 'is_active', 'days_remaining']
    
    fieldsets = (
        ('Subscription Info', {
            'fields': ('user', 'plan', 'payment')
        }),
        ('Status & Dates', {
            'fields': ('status', 'start_date', 'end_date', 'auto_renew', 'cancelled_at')
        }),
        ('Computed Fields', {
            'fields': ('is_active', 'days_remaining'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

"""
Django admin configuration for all models
"""
from django.contrib import admin
from .models import User, Profile, EmailOTP, UserActivity, Notification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'current_tier_display', 'is_staff', 'email_verified', 'created_at']
    list_filter = ['is_staff', 'email_verified', 'created_at']
    search_fields = ['username', 'email']
    readonly_fields = ['created_at', 'updated_at', 'current_tier_display']
    
    def current_tier_display(self, obj):
        """Display computed tier from subscriptions"""
        return obj.current_tier
    current_tier_display.short_description = 'Tier'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('username', 'email', 'phone', 'email_verified')
        }),
        ('Access Control', {
            'fields': ('current_tier_display', 'is_staff')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_tier_display']
    search_fields = ['user__username', 'user__email']
    
    def user_tier_display(self, obj):
        """Display user's current tier"""
        return obj.user.current_tier
    user_tier_display.short_description = 'Tier'


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp', 'purpose', 'is_verified', 'created_at']
    list_filter = ['purpose', 'is_verified', 'created_at']
    search_fields = ['email']
    readonly_fields = ['created_at']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'ip_address', 'created_at']
    list_filter = ['activity', 'created_at']
    search_fields = ['user__username', 'activity']
    readonly_fields = ['created_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    readonly_fields = ['created_at']

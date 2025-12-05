from django.contrib import admin
from .models import User, Profile, PasswordResetRequest, UserActivity, Notification

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'email_verified', 'created_at']
    list_filter = ['email_verified', 'created_at']
    search_fields = ['username', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'plan', 'subscription_start', 'subscription_end']
    list_filter = ['is_paid', 'plan']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user', 'plan']


@admin.register(PasswordResetRequest)
class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'expires_at', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']
    raw_id_fields = ['user']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity', 'ip_address', 'created_at']
    list_filter = ['activity', 'created_at']
    search_fields = ['user__username', 'activity', 'ip_address']
    raw_id_fields = ['user']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    raw_id_fields = ['user']

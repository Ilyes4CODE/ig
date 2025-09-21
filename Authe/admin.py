# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserLogin, UserSnapshot

@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip_address', 'timestamp', 'snapshot_count']
    list_filter = ['timestamp']
    search_fields = ['username', 'ip_address']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def snapshot_count(self, obj):
        count = obj.snapshots.count()
        return count
    snapshot_count.short_description = 'Snapshots'

@admin.register(UserSnapshot)
class UserSnapshotAdmin(admin.ModelAdmin):
    list_display = ['user_login', 'timestamp', 'image_preview']
    list_filter = ['timestamp']
    readonly_fields = ['timestamp', 'image_preview']
    ordering = ['-timestamp']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="75" style="object-fit: cover;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'
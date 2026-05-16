from django.contrib import admin
from .models import SensorData, Alert, SystemSetting


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('topic', 'value', 'location', 'timestamp')
    list_filter = ('topic', 'location', 'timestamp')
    search_fields = ('topic', 'location')
    readonly_fields = ('created_at',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'location', 'timestamp', 'acknowledged')
    list_filter = ('severity', 'location', 'acknowledged', 'timestamp')
    search_fields = ('title', 'message', 'location')
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'description', 'updated_at')
    search_fields = ('key', 'description')
    readonly_fields = ('updated_at',)

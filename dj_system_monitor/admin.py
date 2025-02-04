from django.contrib import admin
from dj_system_monitor.models import ResourceUsage

@admin.register(ResourceUsage)
class ResourceUsageAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "cpu_usage", "memory_usage", "disk_usage", "network_sent", "network_received")
    list_filter = ("timestamp",)
    search_fields = ("cpu_usage", "memory_usage", "disk_usage")
    readonly_fields = ("timestamp",)

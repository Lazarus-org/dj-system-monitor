from django.contrib import admin

from system_monitor.models import ResourceUsage
from system_monitor.settings.conf import config


@admin.register(ResourceUsage, site=config.admin_site_class)
class ResourceUsageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "to_time",
        "cpu_usage",
        "memory_usage",
        "disk_usage",
    )
    list_display_links = ("id", "to_time")
    list_filter = ("from_time", "to_time")
    list_per_page = 10
    search_fields = ("cpu_usage", "memory_usage", "disk_usage")
    readonly_fields = ("from_time", "to_time")

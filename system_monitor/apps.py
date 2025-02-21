from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SystemMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "system_monitor"
    verbose_name = _("Django System Monitor")

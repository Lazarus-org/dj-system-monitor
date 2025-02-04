from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjSystemMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dj_system_monitor"
    verbose_name = _("Django System Monitor")
    

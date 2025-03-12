from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SystemMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "system_monitor"
    verbose_name = _("Django System Monitor")

    def ready(self):
        """This method is called when the application is fully loaded.

        Its main purpose is to perform startup tasks, such as importing
        and registering system checks for validating the configuration
        settings of the app. It ensures that all necessary configurations
        are in place and properly validated when the Django project initializes.

        In this case, it imports the settings checks from the
        `system_monitor.settings` module to validate the configuration
        settings.

        """
        from system_monitor.settings import checks

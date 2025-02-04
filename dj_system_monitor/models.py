from django.db import models
from django.utils.translation import gettext_lazy as _

class ResourceUsage(models.Model):
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text=_("The date and time when the resource usage was recorded."),
        db_comment="Timestamp of the resource usage log."
    )

    cpu_usage = models.FloatField(
        help_text=_("Percentage of CPU usage at the time of logging."),
        db_comment="CPU usage percentage."
    )

    memory_usage = models.FloatField(
        help_text=_("Percentage of RAM usage at the time of logging."),
        db_comment="Memory (RAM) usage percentage."
    )

    disk_usage = models.FloatField(
        help_text=_("Percentage of disk space used at the time of logging."),
        db_comment="Disk usage percentage."
    )

    network_sent = models.FloatField(
        help_text=_("Amount of data sent over the network (in MB)."),
        db_comment="Network data sent in megabytes (MB)."
    )

    network_received = models.FloatField(
        help_text=_("Amount of data received over the network (in MB)."),
        db_comment="Network data received in megabytes (MB)."
    )

    class Meta:
        verbose_name = _("Resource Usage")
        verbose_name_plural = _("Resource Usages")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"CPU: {self.cpu_usage}%, RAM: {self.memory_usage}%, Disk: {self.disk_usage}%"

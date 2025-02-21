from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class ResourceUsage(models.Model):
    from_time = models.DateTimeField(
        verbose_name=_("Start Time"),
        help_text=_("The optional start time of the resource usage monitoring period."),
        db_comment="Start time of the resource usage period (Optional).",
        null=True,
        blank=True,
    )

    to_time = models.DateTimeField(
        verbose_name=_("End Time"),
        help_text=_(
            "The end time of the resource usage monitoring period. Defaults to now if not provided."
        ),
        db_comment="End time of the resource usage period or the time when resource usage was recorded.",
        default=now,
    )

    cpu_usage = models.FloatField(
        verbose_name=_("CPU Usage"),
        help_text=_("Percentage of CPU usage at the time of logging."),
        db_comment="CPU usage percentage.",
    )

    memory_usage = models.FloatField(
        verbose_name=_("Memory Usage"),
        help_text=_("Percentage of RAM usage at the time of logging."),
        db_comment="Memory (RAM) usage percentage.",
    )

    disk_usage = models.FloatField(
        verbose_name=_("Disk Usage"),
        help_text=_("Percentage of disk space used at the time of logging."),
        db_comment="Disk usage percentage.",
    )

    total_network_sent = models.FloatField(
        verbose_name=_("Total Network Sent"),
        help_text=_("Amount of data sent over the network (in MB)."),
        db_comment="Network data sent in megabytes (MB).",
    )

    total_network_received = models.FloatField(
        verbose_name=_("Total Network Received"),
        help_text=_("Amount of data received over the network (in MB)."),
        db_comment="Network data received in megabytes (MB).",
    )

    total_disk_read = models.FloatField(
        verbose_name=_("Total Disk Read"),
        help_text=_("Total amount of data read from the disk (in MB)."),
        db_comment="Total disk read in megabytes (MB).",
    )

    total_disk_write = models.FloatField(
        verbose_name=_("Total Disk Write"),
        help_text=_("Total amount of data written to the disk (in MB)."),
        db_comment="Total disk write in megabytes (MB).",
    )

    class Meta:
        verbose_name = _("Resource Usage")
        verbose_name_plural = _("Resource Usages")
        ordering = ["-to_time"]

    def __str__(self):
        return (
            f"CPU: {self.cpu_usage}%, RAM: {self.memory_usage}%, "
            f"Disk: {self.disk_usage}%, Network Sent: {self.total_network_sent}MB, "
            f"Network Received: {self.total_network_received}MB"
        )

import psutil
from django.core.management.base import BaseCommand
from dj_system_monitor.models import ResourceUsage

class Command(BaseCommand):
    help = "Collect system resource usage metrics"

    def handle(self, *args, **kwargs):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        network_sent = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        network_received = net_io.bytes_recv / (1024 * 1024)  # Convert to MB

        ResourceUsage.objects.create(
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_sent=network_sent,
            network_received=network_received
        )

        self.stdout.write(self.style.SUCCESS("System metrics collected successfully."))

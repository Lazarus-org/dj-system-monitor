import pytest

from system_monitor.models import ResourceUsage


@pytest.fixture
def resource_usage() -> ResourceUsage:
    """
    Fixture to create a ResourceUsage instance.
    """
    return ResourceUsage.objects.create(
        cpu_usage=10,
        memory_usage=35,
        disk_usage=20,
        total_network_sent=2,
        total_network_received=43,
        total_disk_read=14.5,
        total_disk_write=0.6,
    )

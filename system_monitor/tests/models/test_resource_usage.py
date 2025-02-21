import sys

import pytest

from system_monitor.models import ResourceUsage
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.models,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestResourceUsageModel:
    """
    Test suite for the ResourceUsage model.
    """

    def test_str_method(self, resource_usage: ResourceUsage) -> None:
        """
        Test that the __str__ method returns the correct string representation of a resource usage.

        Asserts:
        -------
            - The string representation of the resource includes the name.
        """
        expected_str = (
            f"CPU: {resource_usage.cpu_usage}%, RAM: {resource_usage.memory_usage}%, "
            f"Disk: {resource_usage.disk_usage}%, Network Sent: {resource_usage.total_network_sent}MB, "
            f"Network Received: {resource_usage.total_network_received}MB"
        )
        assert (
            str(resource_usage) == expected_str
        ), f"Expected the __str__ method to return '{expected_str}', but got '{str(resource_usage)}'."

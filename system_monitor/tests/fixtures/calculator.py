import pytest

from system_monitor.calculator import SystemMetricsCalculator


@pytest.fixture
def calculator():
    """Fixture to provide a fresh SystemMetricsCalculator instance."""
    return SystemMetricsCalculator()

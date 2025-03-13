import sys
import time

import pytest
from system_monitor.calculator import SystemMetricsCalculator
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.calculator,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestSystemMetricsCalculator:
    """
    Tests for the SystemMetricsCalculator class, focusing on live_metrics behavior with negative time_diff.
    """

    def test_live_metrics_with_negative_time_diff(
        self, calculator: SystemMetricsCalculator
    ):
        """
        Test the live_metrics method when time_diff is negative.

        This test manually sets a future time as the previous_time using _update_previous_counters,
        then calls live_metrics with the current time, resulting in a negative time_diff.
        It verifies that metrics affected by division (network and disk speeds) are zeroed out.

        Args:
        ----
            calculator (SystemMetricsCalculator): The calculator instance to test.

        Asserts:
        --------
            Network and disk speed metrics are zero due to negative time_diff.
            Other metrics (cpu_usage, memory_usage, disk_usage) are valid and non-zero.
        """
        # Get current system time
        current_time = time.time()

        # Simulate a future previous_time by setting it 10 seconds ahead
        future_time = current_time + 10
        current_net_io = calculator.previous_net_io  # Use initial net_io
        current_disk_io = calculator.previous_disk_io  # Use initial disk_io
        calculator._update_previous_counters(
            current_net_io, current_disk_io, future_time
        )

        # Call live_metrics with current time, making time_diff negative
        metrics = calculator.live_metrics()

        # Assert that metrics involving division by time_diff are zero
        assert (
            metrics["network_sent"] == 0.0
        ), "Network sent should be 0 due to negative time_diff."
        assert (
            metrics["network_received"] == 0.0
        ), "Network received should be 0 due to negative time_diff."
        assert (
            metrics["disk_read_speed"] == 0.0
        ), "Disk read speed should be 0 due to negative time_diff."
        assert (
            metrics["disk_write_speed"] == 0.0
        ), "Disk write speed should be 0 due to negative time_diff."

        # Assert that other metrics are still valid and non-zero
        assert (
            isinstance(metrics["cpu_usage"], float) and metrics["cpu_usage"] >= 0
        ), "CPU usage should be valid."
        assert (
            isinstance(metrics["memory_usage"], float) and metrics["memory_usage"] > 0
        ), "Memory usage should be non-zero."
        assert (
            isinstance(metrics["disk_usage"], float) and metrics["disk_usage"] > 0
        ), "Disk usage should be non-zero."
        assert metrics["disk_active_time"] is None or isinstance(
            metrics["disk_active_time"], float
        ), "Disk active time should be None or a float."

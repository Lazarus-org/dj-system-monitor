import sys

import pytest
from django.core.management import call_command
from django.utils.timezone import now, make_aware, get_current_timezone
from datetime import datetime, timedelta, time
from system_monitor.models import ResourceUsage
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.commands,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestResourceUsageCommand:
    """
    Tests for the custom management command that calculates and logs resource usage metrics.
    """

    def test_command_with_default_arguments(self):
        """
        Test the command with default arguments (no --until and default interval_minutes).
        """
        # Call the command
        call_command("collect_metrics")

        # Verify that a ResourceUsage instance was created
        record = ResourceUsage.objects.first()
        assert record is not None, "ResourceUsage instance should be created."

        # Verify that the timestamps are set correctly
        assert (
            record.from_time <= record.to_time
        ), "from_time should be less than or equal to to_time."

    def test_command_with_custom_until_time(self):
        """
        Test the command with a custom --until time.
        """
        # Define a custom time in the future
        custom_time = (now() + timedelta(seconds=2)).time().strftime("%H:%M:%S")

        # Call the command with the custom --until time
        call_command("collect_metrics", until=custom_time)

        # Verify that a ResourceUsage instance was created
        record = ResourceUsage.objects.first()
        assert record is not None, "ResourceUsage instance should be created."

        # Verify that the to_time is set correctly
        expected_to_time = make_aware(
            datetime.combine(now().date(), time.fromisoformat(custom_time)),
            get_current_timezone(),
        ).astimezone(get_current_timezone())
        assert (
            record.to_time == expected_to_time
        ), "to_time should match the custom --until time."

    def test_command_with_invalid_until_time_format(self, capsys):
        """
        Test the command with an invalid --until time format.
        """
        invalid_time = "25:70:80"  # Invalid time format

        # Call the command
        call_command("collect_metrics", until=invalid_time)

        # Capture stderr output
        captured = capsys.readouterr()
        assert (
            "Invalid date format for --until. Use 'HH:MM:SS'." in captured.err
        ), "Expected error message for invalid time format."

    def test_command_with_past_until_time(self, capsys):
        """
        Test the command with a --until time that is in the past.
        """
        past_time = (now() - timedelta(minutes=10)).time().strftime("%H:%M:%S")

        # Call the command
        call_command("collect_metrics", until=past_time)

        # Capture stderr output
        captured = capsys.readouterr()
        assert (
            "The --until must be in the future time." in captured.err
        ), "Expected error message for past time."

    def test_command_with_metrics_calculation_error(self, monkeypatch, capsys):
        """
        Test the command when an error occurs during metrics calculation.
        """

        # Mock the SystemMetricsCalculator to raise an exception
        def mock_calculate_metrics(*args, **kwargs):
            raise Exception("Metrics calculation failed.")

        monkeypatch.setattr(
            "system_monitor.calculator.SystemMetricsCalculator.calculate_metrics_over_time",
            mock_calculate_metrics,
        )

        # Call the command
        call_command("collect_metrics")

        # Capture stderr output
        captured = capsys.readouterr()
        assert (
            "An error occurred: Metrics calculation failed." in captured.err
        ), "Expected error message for metrics calculation failure."

    def test_command_with_empty_metrics_in_calculate_metrics_over_time(
        self, monkeypatch, capsys
    ):
        """
        Test the command when no metrics are collected in calculate_metrics_over_time.
        """

        def mock_calculate_metrics_over_time(self, to_time, interval_minutes=1):
            return {
                "to_time": to_time,
                "avg_cpu_usage": 0.0,  # Default due to empty metrics_list
                "avg_memory_usage": 0.0,  # Default due to empty metrics_list
                "last_disk_usage": 80.0,
                "total_network_sent": 10.0,
                "total_network_received": 15.0,
                "total_disk_read": 5.0,
                "total_disk_write": 7.0,
            }

        monkeypatch.setattr(
            "system_monitor.calculator.SystemMetricsCalculator.calculate_metrics_over_time",
            mock_calculate_metrics_over_time,
        )

        future_time = (now() + timedelta(seconds=2)).time().strftime("%H:%M:%S")
        call_command("collect_metrics", until=future_time)
        record = ResourceUsage.objects.first()
        assert record is not None, "ResourceUsage instance should be created."
        assert record.cpu_usage == 0.0, "Avg CPU usage should be 0 for empty metrics."
        assert (
            record.memory_usage == 0.0
        ), "Avg memory usage should be 0 for empty metrics."
        # Verify logging
        # captured = capsys.readouterr()
        # assert (
        #         "No metrics collected; returning default values." in captured.err
        # ), "Expected warning for empty metrics list."

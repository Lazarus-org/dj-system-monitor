import logging
import time
from datetime import datetime
from typing import Dict, Optional, Tuple

import psutil
from django.utils import timezone

logger = logging.getLogger(__name__)


class SystemMetricsCalculator:
    """Class for calculating live and time-based system metrics like CPU,
    memory, disk, and network usage."""

    def __init__(self):
        """Initialize the calculator with previous network and disk I/O
        counters and the previous time.

        This helps calculate changes between subsequent metric
        collections.

        """
        self.previous_net_io: psutil._common.snetio = psutil.net_io_counters()
        self.previous_disk_io: psutil._common.sdiskio = psutil.disk_io_counters()
        self.previous_time: float = time.time()

    @staticmethod
    def _bytes_to_mb(bytes_value: int) -> float:
        """Convert bytes to megabytes.

        Args:
            bytes_value (int): The value in bytes to be converted.

        Returns:
            float: The equivalent value in megabytes, rounded to two decimal places.

        """
        return round(bytes_value / (1024**2), 2)

    def _calculate_network_metrics(
        self, current_net_io: psutil._common.snetio, time_diff: float
    ) -> Tuple[float, float]:
        """Calculate network sent and received speeds over the given time
        interval.

        Args:
            current_net_io (psutil._common.snetio): Current network I/O counters.
            time_diff (float): The time difference between metric collections.

        Returns:
            Tuple[float, float]: The network sent and received speeds in MB/s.

        """
        if time_diff <= 0:
            logger.warning(
                "Time difference is zero or negative; returning 0 for network metrics."
            )
            return 0.0, 0.0

        network_sent = (
            self._bytes_to_mb(
                current_net_io.bytes_sent - self.previous_net_io.bytes_sent
            )
            / time_diff
        )
        network_received = (
            self._bytes_to_mb(
                current_net_io.bytes_recv - self.previous_net_io.bytes_recv
            )
            / time_diff
        )
        return round(network_sent, 2), round(network_received, 2)

    def _calculate_disk_metrics(
        self, current_disk_io: psutil._common.sdiskio, time_diff: float
    ) -> Tuple[float, float, Optional[float]]:
        """Calculate disk read and write speeds and disk active time.

        Args:
            current_disk_io (psutil._common.sdiskio): Current disk I/O counters.
            time_diff (float): The time difference between metric collections.

        Returns:
            Tuple[float, float, Optional[float]]: Disk read and write speeds in MB/s, and disk active time as a percentage.

        """
        if time_diff <= 0:
            logger.warning(
                "Time difference is zero or negative; returning 0 for disk metrics."
            )
            return 0.0, 0.0, None

        disk_read_speed = (
            self._bytes_to_mb(
                current_disk_io.read_bytes - self.previous_disk_io.read_bytes
            )
            / time_diff
        )
        disk_write_speed = (
            self._bytes_to_mb(
                current_disk_io.write_bytes - self.previous_disk_io.write_bytes
            )
            / time_diff
        )
        disk_active_time = (
            round(
                (current_disk_io.busy_time - self.previous_disk_io.busy_time)
                / (time_diff * 1000)
                * 100,
                2,
            )
            if hasattr(current_disk_io, "busy_time")
            else None
        )
        return round(disk_read_speed, 2), round(disk_write_speed, 2), disk_active_time

    def _update_previous_counters(
        self,
        current_net_io: psutil._common.snetio,
        current_disk_io: psutil._common.sdiskio,
        current_time: float,
    ) -> None:
        """Update the previous network, disk I/O counters, and time for the
        next calculation.

        Args:
            current_net_io (psutil._common.snetio): Current network I/O counters.
            current_disk_io (psutil._common.sdiskio): Current disk I/O counters.
            current_time (float): The current time in seconds since the epoch.

        """
        self.previous_net_io = current_net_io
        self.previous_disk_io = current_disk_io
        self.previous_time = current_time

    def live_metrics(self) -> Dict[str, Optional[float]]:
        """Calculate and return live system metrics.

        Returns:
            Dict[str, Optional[float]]: A dictionary containing the following metrics:
                - "cpu_usage": CPU usage percentage.
                - "memory_usage": Memory usage percentage.
                - "disk_usage": Disk usage percentage.
                - "network_sent": Network sent speed in MB/s.
                - "network_received": Network received speed in MB/s.
                - "disk_read_speed": Disk read speed in MB/s.
                - "disk_write_speed": Disk write speed in MB/s.
                - "disk_active_time": Disk active time as a percentage.

        """
        current_net_io = psutil.net_io_counters()
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        time_diff = current_time - self.previous_time

        network_sent, network_received = self._calculate_network_metrics(
            current_net_io, time_diff
        )
        disk_read_speed, disk_write_speed, disk_active_time = (
            self._calculate_disk_metrics(current_disk_io, time_diff)
        )

        self._update_previous_counters(current_net_io, current_disk_io, current_time)

        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage("/").percent,
            "network_sent": network_sent,
            "network_received": network_received,
            "disk_read_speed": disk_read_speed,
            "disk_write_speed": disk_write_speed,
            "disk_active_time": disk_active_time,
        }

    def calculate_metrics_over_time(
        self, to_time: datetime, interval_minutes: int = 1
    ) -> Dict[str, float]:
        """Calculate metrics over a specified time range and compute averages
        or totals.

        Args:
            to_time (datetime): End time for the metrics collection.
            interval_minutes (int, optional): Interval between metric collections, in minutes. Defaults to 1.

        Returns:
            Dict[str, float]: A dictionary containing the following aggregated metrics:
                - "to_time": The end time for the metrics collection.
                - "avg_cpu_usage": Average CPU usage percentage.
                - "avg_memory_usage": Average memory usage percentage.
                - "last_disk_usage": Last recorded disk usage percentage.
                - "total_network_sent": Total network data sent in MB.
                - "total_network_received": Total network data received in MB.
                - "total_disk_read": Total disk data read in MB.
                - "total_disk_write": Total disk data written in MB.

        """
        to_time = (
            timezone.make_aware(to_time) if not timezone.is_aware(to_time) else to_time
        )
        logger.info(
            "Starting metrics calculation until %s with an interval of %s minutes.",
            to_time,
            interval_minutes,
        )

        initial_net_io = psutil.net_io_counters()
        initial_disk_io = psutil.disk_io_counters()

        metrics_list = [
            {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
            }
        ]

        while timezone.now() < to_time:
            time.sleep(interval_minutes * 60)
            metrics = {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
            }
            metrics_list.append(metrics)
            logger.debug(
                "Collected metrics - CPU usage: %s%%, Memory usage: %s%%",
                metrics["cpu_usage"],
                metrics["memory_usage"],
            )

        final_net_io = psutil.net_io_counters()
        final_disk_io = psutil.disk_io_counters()

        total_network_sent = self._bytes_to_mb(
            final_net_io.bytes_sent - initial_net_io.bytes_sent
        )
        total_network_received = self._bytes_to_mb(
            final_net_io.bytes_recv - initial_net_io.bytes_recv
        )
        total_disk_read = self._bytes_to_mb(
            final_disk_io.read_bytes - initial_disk_io.read_bytes
        )
        total_disk_write = self._bytes_to_mb(
            final_disk_io.write_bytes - initial_disk_io.write_bytes
        )

        avg_cpu_usage = round(
            sum(m["cpu_usage"] for m in metrics_list) / len(metrics_list), 2
        )
        avg_memory_usage = round(
            sum(m["memory_usage"] for m in metrics_list) / len(metrics_list), 2
        )

        logger.info(
            "Final metrics calculated - Avg CPU usage: %s%%, Avg Memory usage: %s%%",
            avg_cpu_usage,
            avg_memory_usage,
        )

        return {
            "to_time": to_time,
            "avg_cpu_usage": avg_cpu_usage,
            "avg_memory_usage": avg_memory_usage,
            "last_disk_usage": psutil.disk_usage("/").percent,
            "total_network_sent": total_network_sent,
            "total_network_received": total_network_received,
            "total_disk_read": total_disk_read,
            "total_disk_write": total_disk_write,
        }

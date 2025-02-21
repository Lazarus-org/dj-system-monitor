from datetime import date, datetime, timezone

from django.core.management.base import BaseCommand
from django.utils.timezone import get_current_timezone, make_aware, now

from system_monitor.calculator import SystemMetricsCalculator
from system_monitor.models import ResourceUsage


class Command(BaseCommand):
    help = "Calculate and log resource usage metrics."

    def add_arguments(self, parser):
        parser.add_argument(
            "--until",
            type=str,
            help="End time for the resource usage monitoring period (format: HH:MM:SS, local time). "
            "If not provided, defaults to now.",
        )
        parser.add_argument(
            "--interval_minutes",
            type=float,
            default=1,
            help="Interval in minutes for collecting metrics. Default is 1 minute.",
        )

    def handle(self, *args, **kwargs):
        # Get the arguments
        from_time = now()
        to_time_str = kwargs.get("until")
        interval_minutes = kwargs.get("interval_minutes")

        # Step 1: Handle `to_time`
        if to_time_str:
            if to_time_str:
                try:
                    # Parse the time string
                    user_time = datetime.strptime(to_time_str, "%H:%M:%S").time()

                    # Combine with today's date and make it aware of the local timezone
                    naive_to_time = datetime.combine(date.today(), user_time)
                    local_timezone = get_current_timezone()
                    to_time_local = make_aware(naive_to_time, local_timezone)

                    # Convert local time to UTC
                    to_time_utc = to_time_local.astimezone(timezone.utc)

                    if to_time_utc < now():
                        self.stderr.write(
                            self.style.ERROR("The --until must be in the future time.")
                        )
                        return

                    # Calculate the actual interval if `to_time` is less than a minute away
                    time_difference = (to_time_utc - from_time).total_seconds()
                    if time_difference < 60:
                        interval_minutes = max(time_difference / 60, 0.1)
                except ValueError:
                    self.stderr.write(
                        self.style.ERROR(
                            "Invalid date format for --until. Use 'HH:MM:SS'."
                        )
                    )
                    return
        else:
            # Default to current time (already in UTC)
            to_time_utc = now()

        # Step 2: Calculate metrics
        try:
            calculator = SystemMetricsCalculator()
            metrics = calculator.calculate_metrics_over_time(
                to_time=to_time_utc, interval_minutes=interval_minutes
            )

            # Step 3: Create and save a new ResourceUsage instance
            ResourceUsage.objects.create(
                from_time=from_time,
                to_time=to_time_utc,
                cpu_usage=metrics["avg_cpu_usage"],
                memory_usage=metrics["avg_memory_usage"],
                disk_usage=metrics["last_disk_usage"],
                total_network_sent=metrics["total_network_sent"],
                total_network_received=metrics["total_network_received"],
                total_disk_read=metrics["total_disk_read"],
                total_disk_write=metrics["total_disk_write"],
            )

            self.stdout.write(
                self.style.SUCCESS("Resource usage metrics successfully recorded.")
            )

        except Exception as e:  # pylint: disable=W0718
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))

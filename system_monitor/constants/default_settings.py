from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class DefaultAdminSettings:
    admin_site_class: Optional[str] = None


@dataclass(frozen=True)
class DefaultThrottleSettings:
    authenticated_user_throttle_rate: str = "30/minute"
    staff_user_throttle_rate: str = "100/minute"
    throttle_class: str = "system_monitor.api.throttlings.RoleBasedUserRateThrottle"


@dataclass(frozen=True)
class DefaultPaginationAndFilteringSettings:
    pagination_class: str = (
        "system_monitor.api.paginations.DefaultLimitOffSetPagination"
    )
    ordering_fields: List[str] = field(
        default_factory=lambda: [
            "id",
            "to_time",
            "cpu_usage",
            "memory_usage",
            "disk_usage",
            "total_network_sent",
            "total_network_received",
        ]
    )
    search_fields: List[str] = field(default_factory=lambda: ["id"])


# pylint: disable=too-many-instance-attributes
@dataclass(frozen=True)
class DefaultAPISettings:
    allow_list: bool = True
    allow_retrieve: bool = True
    extra_permission_class: Optional[str] = None
    parser_classes: List[str] = field(
        default_factory=lambda: [
            "rest_framework.parsers.JSONParser",
            "rest_framework.parsers.MultiPartParser",
            "rest_framework.parsers.FormParser",
        ]
    )
    resource_usage_serializer_class = None


admin_settings = DefaultAdminSettings()
throttle_settings = DefaultThrottleSettings()
pagination_and_filter_settings = DefaultPaginationAndFilteringSettings()
api_settings = DefaultAPISettings()

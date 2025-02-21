from typing import List

from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from system_monitor.api.serializers.resource_usage import ResourceUsageSerializer
from system_monitor.calculator import SystemMetricsCalculator
from system_monitor.mixins.api.config_api_attrs import ConfigureAttrsMixin
from system_monitor.mixins.api.control_api_methods import ControlAPIMethodsMixin
from system_monitor.models import ResourceUsage
from system_monitor.settings.conf import config


# pylint: disable=too-many-ancestors
class ResourceUsageViewSet(
    ReadOnlyModelViewSet, ControlAPIMethodsMixin, ConfigureAttrsMixin
):

    queryset = ResourceUsage.objects.all()
    serializer_class = config.resource_usage_serializer_class or ResourceUsageSerializer
    filter_backends: List = [OrderingFilter, SearchFilter]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the viewset and configure attributes based on settings.

        Disables the 'list', 'retrieve', 'create', 'update', and 'destroy' methods
        if their corresponding settings are set to `False`.

        """
        super().__init__(*args, **kwargs)
        self.configure_attrs()
        self.metrics_calculator = SystemMetricsCalculator()

        # Mapping of configuration settings to the corresponding methods to disable
        config_method_mapping = {
            "api_allow_list": "LIST",
            "api_allow_retrieve": "RETRIEVE",
        }

        # Disable methods based on configuration settings
        for config_setting, method in config_method_mapping.items():
            if not getattr(config, config_setting, True):
                self.disable_methods([method])

    @action(detail=False, methods=["get"])
    def realtime(self, request):
        data = self.metrics_calculator.live_metrics()
        return Response(data)

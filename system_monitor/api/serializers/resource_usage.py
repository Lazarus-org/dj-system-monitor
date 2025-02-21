from rest_framework.serializers import ModelSerializer

from system_monitor.models import ResourceUsage


class ResourceUsageSerializer(ModelSerializer):
    class Meta:
        model = ResourceUsage
        fields = "__all__"

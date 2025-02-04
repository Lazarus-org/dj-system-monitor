from rest_framework import serializers
from dj_system_monitor.models import ResourceUsage

class ResourceUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceUsage
        fields = '__all__'

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from dj_system_monitor.models import ResourceUsage
from dj_system_monitor.serializers import ResourceUsageSerializer
import psutil

class ResourceUsageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ResourceUsage.objects.all().order_by('-timestamp')[:100]
    serializer_class = ResourceUsageSerializer

    @action(detail=False, methods=['get'])
    def realtime(self, request):
        data = {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "network_sent": psutil.net_io_counters().bytes_sent / (1024 * 1024),
            "network_received": psutil.net_io_counters().bytes_recv / (1024 * 1024),
        }
        return Response(data)



from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard.html")
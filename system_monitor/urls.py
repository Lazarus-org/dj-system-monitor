from django.urls import path
from rest_framework.routers import DefaultRouter

from system_monitor.api.views.resource_usage import ResourceUsageViewSet
from system_monitor.views import DashboardView

router = DefaultRouter()
router.register("metrics", ResourceUsageViewSet, basename="metrics")

urlpatterns = router.urls
urlpatterns += [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]

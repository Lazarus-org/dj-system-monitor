from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_system_monitor.views import ResourceUsageViewSet, dashboard_view

router = DefaultRouter()
router.register(r'metrics', ResourceUsageViewSet, basename='metrics')

urlpatterns = router.urls
urlpatterns += [
    path('dashboard/', dashboard_view, name='dashboard'),
]
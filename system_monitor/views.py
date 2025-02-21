from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated

from system_monitor.settings.conf import config


class DashboardView(TemplateView):
    template_name = "dashboard.html"
    permission_classes = [IsAuthenticated, config.api_extra_permission_class]

    def dispatch(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Instantiates and returns the list of permissions that this view
        requires."""
        return [permission() for permission in self.permission_classes if permission]

    def check_permissions(self, request):
        """Check if the request should be permitted.

        Raises an appropriate exception if the request is not permitted.

        """
        for permission in self.get_permissions():
            if not permission.has_permission(request, self):
                raise PermissionDenied()

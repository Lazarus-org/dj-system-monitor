import sys

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny

from system_monitor.settings.conf import config
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestDashboardView:
    """
    Tests for the DashboardView using pytest.

    This test class verifies the behavior of the DashboardView, ensuring that:
    - Authenticated users can access the view.
    - Unauthenticated users are denied access.
    - Additional permissions (if configured) are enforced.
    - The correct template is rendered.
    """

    def test_authenticated_user_access(self, request_factory, user, view, url):
        """
        Test that an authenticated user can access the DashboardView.
        """
        request = request_factory.get(url)
        request.user = user  # Simulate an authenticated user

        response = view(request)
        assert (
            response.status_code == 200
        ), "Authenticated user should get a 200 OK response."

    def test_unauthenticated_user_access(self, request_factory, view, url):
        """
        Test that an unauthenticated user is denied access to the DashboardView.
        """
        request = request_factory.get(url)
        request.user = AnonymousUser()  # Simulate an unauthenticated user

        with pytest.raises(PermissionDenied):
            view(request)

    def test_additional_permissions_enforced(self, request_factory, user, view, url):
        """
        Test that additional permissions (if configured) are enforced.
        """
        # Set an additional permission class (e.g., AllowAny)
        config.api_extra_permission_class = AllowAny

        request = request_factory.get(url)
        request.user = user  # Simulate an authenticated user

        response = view(request)
        assert (
            response.status_code == 200
        ), "Additional permissions should allow access."

        # Reset the additional permission class to avoid side effects
        config.api_extra_permission_class = None

    def test_template_rendering(self, request_factory, user, view, url):
        """
        Test that the correct template is rendered for the DashboardView.
        """
        request = request_factory.get(url)
        request.user = user  # Simulate an authenticated user

        response = view(request)
        assert (
            response.status_code == 200
        ), "Template rendering should return a 200 OK response."
        assert (
            response.template_name[0] == "dashboard.html"
        ), "The correct template should be rendered."

import pytest
from rest_framework.test import APIClient

from system_monitor.views import DashboardView


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to initialize the Django REST Framework APIClient for testing.

    :return: An instance of APIClient to make HTTP requests in tests.
    """
    return APIClient()


@pytest.fixture
def view():
    """Fixture to provide the DashboardView as a callable view."""
    return DashboardView.as_view()


@pytest.fixture
def url():
    """Fixture to provide the URL for the dashboard view."""
    return "/dashboard/"

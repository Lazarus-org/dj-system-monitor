import pytest
from django.contrib.admin import AdminSite
from django.test import RequestFactory

from system_monitor.admin import ResourceUsageAdmin
from system_monitor.models import ResourceUsage


@pytest.fixture
def request_factory() -> RequestFactory:
    """
    Fixture to provide an instance of RequestFactory.

    Returns:
    -------
        RequestFactory: An instance of Django's RequestFactory.
    """
    return RequestFactory()


@pytest.fixture
def admin_site() -> AdminSite:
    """
    Fixture to provide an instance of AdminSite.

    Returns:
    -------
        AdminSite: An instance of Django's AdminSite.
    """
    return AdminSite()


@pytest.fixture
def resource_usage_admin(admin_site: AdminSite) -> ResourceUsageAdmin:
    """
    Fixture to provide an instance of ResourceUsageAdmin.

    Args:
    ----
        admin_site (AdminSite): An instance of Django's AdminSite.

    Returns:
    -------
        ResourceUsageAdmin: An instance of ResourceUsageAdmin.
    """
    return ResourceUsageAdmin(ResourceUsage, admin_site)

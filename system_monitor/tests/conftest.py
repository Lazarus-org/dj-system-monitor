import pytest
from system_monitor.tests.setup import configure_django_settings
from system_monitor.tests.fixtures import (
    view,
    url,
    user,
    admin_user,
    admin_site,
    request_factory,
    api_client,
    resource_usage_admin,
    resource_usage,
    calculator,
)

import sys

import pytest

from system_monitor.admin import ResourceUsageAdmin
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.admin,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


@pytest.mark.django_db
class TestResourceUsageAdmin:
    """
    Tests for the ResourceUsageAdmin class in the Django admin interface.

    This test class verifies the configuration of the ResourceUsageAdmin,
    ensuring that the correct fields are displayed, filtered, searchable,
    and marked as read-only in the Django admin interface.

    Tests:
    -------
    - test_list_display: Verifies that the correct fields are displayed in the list view.
    - test_list_filter: Checks that the correct fields are available for filtering in the list view.
    - test_search_fields: Ensures that the correct fields are searchable in the admin interface.
    - test_readonly_fields: Confirms that the correct fields are marked as read-only in the admin form.
    """

    def test_list_display(self, resource_usage_admin: ResourceUsageAdmin) -> None:
        """
        Test the list display configuration of the ResourceUsageAdmin.

        This test checks that the fields displayed in the list view of the
        ResourceUsageAdmin match the expected fields.

        Args:
        ----
            resource_usage_admin (ResourceUsageAdmin): The admin class instance
            being tested.

        Asserts:
        --------
            The list_display attribute of the resource_usage_admin matches the
            expected list of fields.
        """
        expected_list_display = (
            "id",
            "to_time",
            "cpu_usage",
            "memory_usage",
            "disk_usage",
        )
        assert resource_usage_admin.list_display == expected_list_display

    def test_list_filter(self, resource_usage_admin: ResourceUsageAdmin) -> None:
        """
        Test the list filter configuration of the ResourceUsageAdmin.

        This test checks that the fields available for filtering in the list
        view of the ResourceUsageAdmin match the expected fields.

        Args:
        ----
            resource_usage_admin (ResourceUsageAdmin): The admin class instance
            being tested.

        Asserts:
        --------
            The list_filter attribute of the resource_usage_admin matches the
            expected list of filter fields.
        """
        expected_list_filter = ("from_time", "to_time")
        assert resource_usage_admin.list_filter == expected_list_filter

    def test_search_fields(self, resource_usage_admin: ResourceUsageAdmin) -> None:
        """
        Test the search fields configuration of the ResourceUsageAdmin.

        This test checks that the fields available for searching in the admin
        interface match the expected fields.

        Args:
        ----
            resource_usage_admin (ResourceUsageAdmin): The admin class instance
            being tested.

        Asserts:
        --------
            The search_fields attribute of the resource_usage_admin matches the
            expected list of searchable fields.
        """
        expected_search_fields = ("cpu_usage", "memory_usage", "disk_usage")
        assert resource_usage_admin.search_fields == expected_search_fields

    def test_readonly_fields(self, resource_usage_admin: ResourceUsageAdmin) -> None:
        """
        Test the read-only fields configuration of the ResourceUsageAdmin.

        This test checks that the fields marked as read-only in the admin form
        match the expected fields.

        Args:
        ----
            resource_usage_admin (ResourceUsageAdmin): The admin class instance
            being tested.

        Asserts:
        --------
            The readonly_fields attribute of the resource_usage_admin matches the
            expected list of read-only fields.
        """
        expected_readonly_fields = ("from_time", "to_time")
        assert resource_usage_admin.readonly_fields == expected_readonly_fields

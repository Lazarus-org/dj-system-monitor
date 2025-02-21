import sys
from unittest.mock import Mock

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.test import APIClient

from system_monitor.models import ResourceUsage
from system_monitor.settings.conf import config
from system_monitor.tests.constants import PYTHON_VERSION, PYTHON_VERSION_REASON

pytestmark = [
    pytest.mark.api,
    pytest.mark.api_views,
    pytest.mark.skipif(sys.version_info < PYTHON_VERSION, reason=PYTHON_VERSION_REASON),
]


class TestResourceUsageViewSet:
    """
    Tests for the ResourceUsageViewSet API endpoints.

    This test class verifies the behavior of the ResourceUsageViewSet,
    ensuring that the list and retrieve methods function correctly
    under various configurations and user permissions.

    Tests:
    -------
    - test_list_resource_usage: Verifies that the list endpoint returns
      a 200 OK status and includes results when allowed.
    - test_retrieve_resource_usage: Checks that the retrieve endpoint
      returns a 200 OK status and the correct resource when allowed.
    - test_list_resource_usage_disabled: Tests that the list endpoint
      returns a 405 Method Not Allowed status when disabled via configuration.
    - test_retrieve_resource_usage_disabled: Tests that the retrieve
      endpoint returns a 405 Method Not Allowed status when disabled
      via configuration.
    - test_realtime_action: Tests that the realtime action returns
      live metrics data with a 200 OK status.
    """

    def test_list_resource_usage(
        self,
        api_client: APIClient,
        admin_user: User,
        monkeypatch: Mock,
        resource_usage: ResourceUsage,
    ):
        """
        Test the list endpoint for ResourceUsage.

        This test checks that the list method returns a 200 OK status
        and includes results when the API is allowed to list resources.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User ): The admin user for authentication.
            monkeypatch (Mock): Mock object for patching during tests.
            resource_usage (ResourceUsage): A sample ResourceUsage instance
            to ensure data is present.

        Asserts:
        --------
            The response status code is 200.
            The response data contains a 'results' key.
            The 'results' key contains data.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_list = True  # Ensure the list method is allowed

        url = reverse("metrics-list")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "results" in response.data, "Expected 'results' in response data."
        assert len(response.data["results"]) > 0, "Expected data in the results."

    def test_retrieve_resource_usage(
        self,
        api_client: APIClient,
        admin_user: User,
        resource_usage: ResourceUsage,
    ):
        """
        Test the retrieve endpoint for ResourceUsage.

        This test checks that the retrieve method returns a 200 OK status
        and the correct resource data when the API is allowed to retrieve
        resources.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User ): The admin user for authentication.
            resource_usage (ResourceUsage): The ResourceUsage instance to retrieve.

        Asserts:
        --------
            The response status code is 200.
            The response data contains the correct ResourceUsage ID.
        """
        api_client.force_authenticate(user=admin_user)

        config.api_allow_retrieve = True  # Ensure the retrieve method is allowed
        config.exclude_serializer_empty_fields = True  # Testing this option too

        url = reverse("metrics-detail", kwargs={"pk": resource_usage.pk})

        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert (
            response.data["id"] == resource_usage.pk
        ), f"Expected ResourceUsage ID {response.pk}, got {response.data['id']}."

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_list_resource_usage_disabled(
        self, api_client: APIClient, admin_user: User, user: User, is_staff: bool
    ):
        """
        Test the list view when disabled via configuration.

        This test checks that the list method returns a 405 Method Not Allowed
        status when the API is configured to disallow listing resources.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User ): The admin user for authentication.
            user (User ): A regular user for testing permissions.
            is_staff (bool): Indicates whether to authenticate as an admin user or a regular user.

        Asserts:
        --------
            The response status code is 405.
        """
        _user = admin_user if is_staff else user
        api_client.force_authenticate(user=_user)

        config.api_allow_list = False  # Disable the list method

        url = reverse("metrics-list")
        response = api_client.get(url)

        assert (
            response.status_code == 405
        ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_retrieve_resource_usage_disabled(
        self,
        api_client: APIClient,
        admin_user: User,
        user: User,
        resource_usage: ResourceUsage,
    ):
        """
        Test the retrieve view when disabled via configuration.

        This test checks that the retrieve method returns a 405 Method Not Allowed
        status when the API is configured to disallow retrieving resources.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User  ): The admin user for authentication.
            user (User  ): A regular user for testing permissions.
            resource_usage (ResourceUsage): The ResourceUsage instance to retrieve.

        Asserts:
        --------
            The response status code is 405.
        """
        for user in [admin_user, user]:
            api_client.force_authenticate(user=user)

            config.api_allow_retrieve = False  # Disable the retrieve method
            config.api_extra_permission_class = AllowAny  # Also test this config

            url = reverse("metrics-detail", kwargs={"pk": resource_usage.pk})
            response = api_client.get(url)

            assert (
                response.status_code == 405
            ), f"Expected 405 Method Not Allowed, got {response.status_code}."

    def test_realtime_action(
        self,
        api_client: APIClient,
        admin_user: User,
    ):
        """
        Test the realtime action for ResourceUsage.

        This test checks that the realtime action returns a 200 OK status
        and includes live metrics data.

        Args:
        ----
            api_client (APIClient): The API client used to simulate requests.
            admin_user (User): The admin user for authentication.

        Asserts:
        --------
            The response status code is 200.
            The response data contains live metrics data.
        """
        api_client.force_authenticate(user=admin_user)

        url = reverse("metrics-realtime")
        response = api_client.get(url)

        assert (
            response.status_code == 200
        ), f"Expected 200 OK, got {response.status_code}."
        assert "cpu_usage" in response.data, "Expected 'cpu_usage' in response data."
        assert (
            "memory_usage" in response.data
        ), "Expected 'memory_usage' in response data."

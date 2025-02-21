from typing import Any, List

from django.core.checks import Error, register

from system_monitor.settings.conf import config
from system_monitor.validators.config_validators import (
    validate_boolean_setting,
    validate_list_fields,
    validate_optional_path_setting,
    validate_optional_paths_setting,
    validate_throttle_rate,
)


@register()
def check_system_monitor_settings(app_configs: Any, **kwargs: Any) -> List[Error]:
    """Check and validate system monitor settings in the Django configuration.

    This function performs validation of various system monitor-related settings
    defined in the Django settings. It returns a list of errors if any issues are found.

    Parameters:
    -----------
    app_configs : Any
        Passed by Django during checks (not used here).

    kwargs : Any
        Additional keyword arguments for flexibility.

    Returns:
    --------
    List[Error]
        A list of `Error` objects for any detected configuration issues.

    """
    errors: List[Error] = []

    # Validate boolean settings
    errors.extend(
        validate_boolean_setting(
            config.api_allow_list, f"{config.prefix}API_ALLOW_LIST"
        )
    )
    errors.extend(
        validate_boolean_setting(
            config.api_allow_retrieve, f"{config.prefix}API_ALLOW_RETRIEVE"
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_ordering_fields, f"{config.prefix}API_ORDERING_FIELDS"
        )
    )
    errors.extend(
        validate_list_fields(
            config.api_search_fields, f"{config.prefix}API_SEARCH_FIELDS"
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.staff_user_throttle_rate,
            f"{config.prefix}STAFF_USER_THROTTLE_RATE",
        )
    )
    errors.extend(
        validate_throttle_rate(
            config.authenticated_user_throttle_rate,
            f"{config.prefix}AUTHENTICATED_USER_THROTTLE_RATE",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_THROTTLE_CLASS", None),
            f"{config.prefix}API_THROTTLE_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(
                f"{config.prefix}API_RESOURCE_USAGE_SERIALIZER_CLASS", None
            ),
            f"{config.prefix}API_RESOURCE_USAGE_SERIALIZER_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_PAGINATION_CLASS", None),
            f"{config.prefix}API_PAGINATION_CLASS",
        )
    )
    errors.extend(
        validate_optional_paths_setting(
            config.get_setting(f"{config.prefix}API_PARSER_CLASSES", []),
            f"{config.prefix}API_PARSER_CLASSES",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}API_EXTRA_PERMISSION_CLASS", None),
            f"{config.prefix}API_EXTRA_PERMISSION_CLASS",
        )
    )
    errors.extend(
        validate_optional_path_setting(
            config.get_setting(f"{config.prefix}ADMIN_SITE_CLASS", None),
            f"{config.prefix}ADMIN_SITE_CLASS",
        )
    )

    return errors

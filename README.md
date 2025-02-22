# Welcome to the Django System Monitor Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-system-monitor)](https://github.com/lazarus-org/dj-system-monitor/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-system-monitor)](https://pypi.org/project/dj-system-monitor/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-system-monitor)](https://pypi.org/project/dj-system-monitor/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-system-monitor)](https://pypi.org/project/dj-system-monitor/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-system-monitor)](https://github.com/lazarus-org/dj-system-monitor/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-system-monitor)](https://github.com/lazarus-org/dj-system-monitor/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-system-monitor)](https://github.com/lazarus-org/dj-system-monitor)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-system-monitor/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-system-monitor)

[`dj-system-monitor`](https://github.com/lazarus-org/dj-system-monitor/) is a Django package developed by Lazarus to
monitor system resources efficiently. It provides a `ResourceUsage` model to store Usage metrics, a Django `ModelAdmin`
for easy management via the admin panel, and a built-in Dashboard using template view for live monitoring. Additionally,
it offers a Django REST Framework (DRF) API for tracking Resource Usages at the API level.

This package is designed to be flexible and easy to integrate into Django projects, allowing developers to track system
resource usages effectively. Whether you need a simple dashboard or a full-fledged API, `dj-system-monitor` provides the
necessary tools to streamline system monitoring.

## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2
- Django REST Framework: >= 3.14

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[API Guide](#api-guide)**: Detailed information on available APIs and endpoints.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[Settings](#settings)**: Configuration options and settings you can customize.

---

# Quick Start

This section provides a fast and easy guide to getting the `dj-system-monitor` package up and running in your Django
project.
Follow the steps below to quickly set up the package and start using the package.

## 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-system-monitor
```

**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-system-monitor
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-system-monitor
```

## 2. Install Django REST Framework

You need to install Django REST Framework for API support. If it's not already installed in your project, you can
install it via pip:

**Using pip:**

```bash
$ pip install djangorestframework
```

## 3. Add to Installed Apps

After installing the necessary packages, ensure that both `rest_framework` and `system_monitor` are added to
the `INSTALLED_APPS` in your Django `settings.py` file:

```python
INSTALLED_APPS = [
    # ...
    "rest_framework",

    "system_monitor",
    # ...
]
```

## 4. Apply Migrations

Run the following command to apply the necessary migrations:

```shell
python manage.py migrate
```

## 5. Add SystemMonitor API URLs

You can use the API or the Django Template View for Dashboard by Including them in your project’s `urls.py` file:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("system_monitor/", include("system_monitor.urls")),
    # ...
]
```

----

# API Guide

This section provides a detailed overview of the Django System Monitor API, allowing users to manage resource usage
efficiently. The API exposes two main endpoints:

## ResourceUsage API

The ``metrics/`` endpoint provides the following features:

- **List resource usage**:

  Fetches all resource usages. Controlled by the ``SYSTEM_MONITOR_API_ALLOW_LIST`` setting.

- **Retrieve a resource usage**:

  Retrieve a resource usage. This feature is controlled by the ``SYSTEM_MONITOR_API_ALLOW_RETRIEVE`` setting.

---

## Example Responses

Here are some examples of responses for each action:

**List resource usage with default serializer**:

```text
GET /metrics/

Response:
HTTP/1.1 200 OK
Content-Type: application/json

"results": [
    {
            "id": 11,
            "from_time": "2025-02-21T20:07:43.246351+03:30",
            "to_time": "2025-02-21T20:07:43.246359+03:30",
            "cpu_usage": 25.0,
            "memory_usage": 85.0,
            "disk_usage": 10.7,
            "total_network_sent": 0.0,
            "total_network_received": 0.0,
            "total_disk_read": 0.0,
            "total_disk_write": 0.0
        },
        {
            "id": 10,
            "from_time": "2025-02-21T20:06:17.985613+03:30",
            "to_time": "2025-02-21T20:07:00+03:30",
            "cpu_usage": 32.85,
            "memory_usage": 85.1,
            "disk_usage": 10.7,
            "total_network_sent": 0.08,
            "total_network_received": 0.11,
            "total_disk_read": 1.23,
            "total_disk_write": 10.31
        }
]
```

### **Realtime Metrics**

The `realtime` action provides real-time system metrics. This action is accessible via a `GET` request to
the `/metrics/realtime/` endpoint.

#### Example Request:

```text
GET /metrics/realtime/

Response:
HTTP/1.1 200 OK
Content-Type: application/json

{
    "cpu_usage": 25.0,
    "memory_usage": 85.0,
    "disk_usage": 10.7,
    "network_sent": 0.08,
    "network_received": 0.11,
    "disk_read_speed": 1.23,
    "disk_write_speed": 10.31,
    "disk_active_time": 5.5
}
```
**Response Fields**:

- `cpu_usage`: Current CPU usage percentage.

- `memory_usage`: Current memory (RAM) usage percentage.

- `disk_usage`: Current disk usage percentage.

- `network_sent`: Network data sent speed in MB/s.

- `network_received`: Network data received speed in MB/s.

- `disk_read_speed`: Disk read speed in MB/s.

- `disk_write_speed`: Disk write speed in MB/s.

- `disk_active_time`: Disk active time as a percentage.

---

## Throttling

The API includes a built-in throttling mechanism that limits the number of requests a user can make based on their role.
You can customize these throttle limits in the settings file.

To specify the throttle rates for authenticated users and staff members, add the following in your settings:

```ini
SYSTEM_MONITOR_AUTHENTICATED_USER_THROTTLE_RATE = "100/day"
SYSTEM_MONITOR_STAFF_USER_THROTTLE_RATE = "60/minute"
```

These settings limit the number of requests users can make within a given timeframe.

**Note:** You can define custom throttle classes and reference them in your settings.

---

## Ordering and Search

The API supports ordering and searching of metrics.

Options include:

- **Ordering**: Results can be ordered by fields such as `id`, `to_time`, `cpu_usage`, `memory_usage` or other fields.

- **Search**: You can search for fields like `id` or any other fields.

These fields can be customized by adjusting the related configurations in your Django settings.

---

## Pagination

The API supports limit-offset pagination, with configurable minimum, maximum, and default page size limits. This
controls the number of results returned per page.

---

## Permissions

The base permission for all endpoints is ``IsAuthenticated``, meaning users must be logged in to access the API. You can
extend this by creating custom permission classes to implement more specific access control.

For instance, you can allow only specific user roles to perform certain actions.

---

## Parser Classes

The API supports multiple parser classes that control how data is processed. The default parsers include:

- ``JSONParser``
- ``MultiPartParser``
- ``FormParser``

You can modify parser classes by updating the API settings to include additional parsers or customize the existing ones
to suit your project.

----

Each feature can be configured through the Django settings file. For further details, refer to the [Settings](#settings)
section.

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of
the Django admin panels for managing resource usages.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your
Django settings. Otherwise, Django may raise the following error during checks or the ModelAdmin will not accessible in
the Admin panel.

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class
instance

```python
SYSTEM_MONITOR_ADMIN_SITE_CLASS = "path.to.your.custom.site"
```

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
SYSTEM_MONITOR_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-system-monitor` to use your custom admin site for its Admin interface, preventing any errors and
ensuring a smooth integration with the custom admin interface.

# ResourceUsage Admin Panel

The `ResourceUsageAdmin` class provides a comprehensive admin interface for managing resource usage records in the
Django admin panel. Below are the features and functionality of this admin interface.

---

## Features

### List Display

The list view for resource usage records includes the following fields:

- **ID**: The unique identifier for the resource usage record.
- **To Time**: The end time of the resource usage monitoring period.
- **CPU Usage**: The percentage of CPU usage recorded.
- **Memory Usage**: The percentage of memory (RAM) usage recorded.
- **Disk Usage**: The percentage of disk space used.

### List Display Links

The following fields are clickable links to the detailed view of each record:

- **ID**: Links to the detailed view of the resource usage record.
- **To Time**: Links to the detailed view of the resource usage record.

### Filtering

Admins can filter the list of resource usage records based on:

- **From Time**: Filter records by the start time of the monitoring period.
- **To Time**: Filter records by the end time of the monitoring period.

### Search Functionality

Admins can search for resource usage records using:

- **CPU Usage**: Search by CPU usage percentage.
- **Memory Usage**: Search by memory usage percentage.
- **Disk Usage**: Search by disk usage percentage.

### Pagination

The admin list view displays **10 records per page** by default.

### Read-Only Fields

The following fields are marked as read-only in the detailed view:

- **From Time**: The start time of the monitoring period (cannot be edited).
- **To Time**: The end time of the monitoring period (cannot be edited).

----

# Dashboard

## Overview
The dashboard provides a real-time monitoring interface for system resource usage, including CPU, memory, disk, and network activity.

## Access Control
- Only authenticated users with the necessary permissions can access the dashboard.
- Ensure that the required permissions are correctly configured in your settings.

## Features
- **Real-Time Updates**: Resource metrics update dynamically at short intervals.
- **Smooth Visuals**: Animated transitions for a better user experience.
- **Historical Data**: The last few metrics are displayed for trend analysis.

## Usage
1. Navigate to the dashboard URL in your application (default: `/system_monitor/dashboard`).
2. Ensure you are logged in with the necessary permissions.
3. View real-time resource usage metrics, updated automatically.

## Short Polling
- The dashboard uses short polling to fetch updated metrics every few seconds.
- This ensures up-to-date information without overloading the server.

---

## collect_metrics Command

The `collect_metrics` command is designed to collect and store system resource metrics (CPU, memory, disk usage, and network usage) over a specified time period (or live if no `--until` provided). Here's the breakdown of its key functionalities:

### Command Overview

This command calculates and stores CPU, memory, disk, and network usage. The `collect_metrics` command is useful for tracking system performance and resource consumption.

### Optional Arguments

- `--until <HH:MM:SS>`:
  Defines the end time for the monitoring period in the **local time zone**. Defaults to the current time if not provided.

- `--interval_minutes <float>`:
  Defines the interval (in minutes) for collecting metrics (useful if passing `--until` for collecting average metrics in a time range) . The default value is `1` minute.

### Usage

The command can be run using Django's `manage.py` utility:

```bash
$ python manage.py collect_metrics --until 23:59:59 --interval_minutes 5
```

### Command Flow

1. **Current Metrics Collection**:
   - If `--until` is not provided, the command collects system metrics (CPU, memory, disk read/write, and network sent/received usage) for the current time and stores them immediately in the database.

2. **Timed Metrics Collection**:
   - If `--until` is provided, the command will fetch average metrics between the time of running the command and the end time passed as `--until`. For example, if you specify `--until 23:15:00`, it will start collecting metrics from the current time until 23:15:00. During this period, the command collects data at the specified `--interval_minutes` (e.g., every 2 minutes). It will then compute and store:
     - **Average CPU and Memory Usage**: The command aggregates CPU and memory metrics during the time range and saves their averages.
     - **Total Network and Disk Usage**: For network, the total amount of data sent and received is accumulated over the time range. For Disk read/write, the total amount of read and write data is accumulated over the time range, while Disk usage is stored as the last disk space value captured.


### Scheduling the Command

#### Example Using a Cron Job
To schedule the command to run every day to collect the resource usages between a specific time range, add this to the crontab:

```cron
0 15 * * * /path/to/venv/bin/python /path/to/project/manage.py collect_metrics --until 21:30:00 --interval_minutes 5
```

this will run the command every day at 15:00 , and collect the metrics every 5 minute until 21:30, and saves the average to the database.

----

# Settings

This section outlines the available settings for configuring the `dj-system-monitor` package. You can customize these
settings in your Django project's `settings.py` file to tailor the behavior of the system monitor to your
needs.

## Example Settings

Below is an example configuration with default values:

```python

SYSTEM_MONITOR_ADMIN_SITE_CLASS = None
SYSTEM_MONITOR_API_RESOURCE_USAGE_SERIALIZER_CLASS = None
SYSTEM_MONITOR_API_ALLOW_LIST = True
SYSTEM_MONITOR_API_ALLOW_RETRIEVE = False
SYSTEM_MONITOR_AUTHENTICATED_USER_THROTTLE_RATE = "30/minute"
SYSTEM_MONITOR_STAFF_USER_THROTTLE_RATE = "100/minute"
SYSTEM_MONITOR_API_THROTTLE_CLASS = (
    "system_monitor.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"
)
SYSTEM_MONITOR_API_PAGINATION_CLASS = "system_monitor.api.paginations.limit_offset_pagination.DefaultLimitOffSetPagination"
SYSTEM_MONITOR_API_EXTRA_PERMISSION_CLASS = None
SYSTEM_MONITOR_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
SYSTEM_MONITOR_API_ORDERING_FIELDS = [
  "id",
  "to_time",
  "cpu_usage",
  "memory_usage",
  "disk_usage",
  "total_network_sent",
  "total_network_received",
]
SYSTEM_MONITOR_API_SEARCH_FIELDS = ["id"]
```

## Settings Overview

Below is a detailed description of each setting, so you can better understand and tweak them to fit your project's
needs.

### ``SYSTEM_MONITOR_ADMIN_SITE_CLASS``

**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies A custom AdminSite class to apply on Admin interface. This allows for more
customization on Admin interface, enabling you to apply your AdminSite class into `dj-system-monitor` Admin interface.

---

### ``SYSTEM_MONITOR_API_ALLOW_LIST``

**Type**: ``bool``

**Default**: ``True``

**Description**: Allows the listing of resource usage via the API. Set to ``False`` to disable this feature.

---

### ``SYSTEM_MONITOR_API_ALLOW_RETRIEVE``

**Type**: ``bool``

**Default**: ``True``

**Description**: Allows retrieving individual SYSTEM_MONITOR via the API. Set to ``False`` to disable this feature.

---

### ``SYSTEM_MONITOR_AUTHENTICATED_USER_THROTTLE_RATE``

**Type**: ``str``

**Default**: ``"30/minute"``

**Description**: Sets the throttle rate (requests per minute, hour or day) for authenticated users in the API.

---

### ``SYSTEM_MONITOR_STAFF_USER_THROTTLE_RATE``

**Type**: `str`

**Default**: `"100/minute"`

**Description**: Sets the throttle rate (requests per minute, hour or day) for staff (Admin) users in the API.

---

### ``SYSTEM_MONITOR_API_THROTTLE_CLASS``

**Type**: ``str``

**Default**: ``"system_monitor.api.throttlings.role_base_throttle.RoleBasedUserRateThrottle"``

**Description**:  Specifies the throttle class used to limit API requests. Customize this or set it to ``None`` if no
throttling is needed or want to use ``rest_framework`` `DEFAULT_THROTTLE_CLASSES`.

---

### ``SYSTEM_MONITOR_API_RESOURCE_USAGE_SERIALIZER_CLASS``

**Type**: ``str``

**Default**: ``"system_monitor.api.serializers.resourse_usage.ResourceUsageSerializer"``

**Description**: Defines the serializer class used in the API. Customize this if you prefer a different serializer
class.


---

### ``SYSTEM_MONITOR_API_PAGINATION_CLASS``

**Type**: ``str``

**Default**: ``"system_monitor.api.paginations.limit_offset_pagination.DefaultLimitOffSetPagination"``

**Description**: Defines the pagination class used in the API. Customize this if you prefer a different pagination style
or set to ``None`` to disable pagination.

---

### ``SYSTEM_MONITOR_API_EXTRA_PERMISSION_CLASS``

**Type**: ``Optional[str]``

**Default**: ``None``

**Description**: Optionally specifies an additional permission class to extend the base permission (``IsAuthenticated``)
for the API. This allows for more fine-grained access control, enabling you to restrict API access to users with a
specific permission, in addition to requiring authentication.

---

### ``SYSTEM_MONITOR_API_PARSER_CLASSES``

**Type**: ``List[str]``

**Default**:

```python
SYSTEM_MONITOR_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
```

**Description**: Specifies the parsers used to handle API request data formats. You can modify this list to add your
parsers or set ``None`` if no parser needed.

---

### ``SYSTEM_MONITOR_API_ORDERING_FIELDS``

**Type**: ``List[str]``

**Default**: ``["id", "to_time", "cpu_usage", "memory_usage", "disk_usage", "total_network_sent", "total_network_received"]``

**Description**: Specifies the fields available for ordering in API queries, allowing the API responses to be sorted by
these fields. you can see all available fields here

---

### ``SYSTEM_MONITOR_API_SEARCH_FIELDS``

**Type**: ``List[str]``

**Default**: ``["id"]``

**Description**: Specifies the fields that are searchable in the API, allowing users to filter results based on these
fields.

---

### All Available Fields

These are all fields that are available for searching and ordering in the resource usages:

- `id`: Unique identifier of the resource usage (orderable, filterable).
- `from_time`: The optional start time of the resource usage monitoring period (orderable, filterable).
- `to_time`: The end time of the resource usage monitoring period (orderable, filterable).
- `cpu_usage`: Percentage of CPU usage at the time of logging (searchable, filterable).
- `memory_usage`: Percentage of RAM usage at the time of logging (searchable, filterable).
- `disk_usage`: Percentage of disk space used at the time of logging (searchable, filterable).
- `total_network_sent`: Amount of data sent over the network (in MB) (searchable, filterable).
- `total_network_received`: Amount of data received over the network (in MB) (searchable, filterable).
- `total_disk_read`: Total amount of data read from the disk (in MB) (searchable, filterable).
- `total_disk_write`: Total amount of data written to the disk (in MB) (searchable, filterable).

----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-system-monitor`.

### Final Notes:

- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python
  versions.
- **API Integration**: The package is designed for flexibility, allowing you to customize many features based on your
  application's needs.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for
  more details.

If you encounter any issues or have feedback, please reach out via
our [GitHub Issues page](https://github.com/lazarus-org/dj-system-monitor/issues).

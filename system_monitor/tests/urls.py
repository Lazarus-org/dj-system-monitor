from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("system_monitor/", include("system_monitor.urls")),
]

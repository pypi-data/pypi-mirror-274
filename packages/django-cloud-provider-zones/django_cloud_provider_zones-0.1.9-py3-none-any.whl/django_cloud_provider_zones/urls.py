from django.urls import path
from .views import (
    cloud_provider_list_drf,
    cloud_region_list_drf,
    cloud_availability_zone_list_drf,
)

app_name = "django_cloud_provider_zones"
urlpatterns = [
    path(
        "cloud-availability-zones/",
        cloud_availability_zone_list_drf,
        name="cloud-availability-zone-list-drf",
    ),
    path("cloud-regions/", cloud_region_list_drf, name="cloud-region-list-drf"),
    path("cloud-providers/", cloud_provider_list_drf, name="cloud-provider-list-drf"),
]

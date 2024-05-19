"""not ready for production, used for testing"""

from django.forms.models import model_to_dict
from rest_framework import serializers
from .models import CloudProvider, CloudRegion, CloudAvailabilityZone

provider_fields = ("provider",)
region_fields = (
    "provider",
    "geographic_region",
    "cardinality",
    "number",
    "original_region_name",
    "short_name",
    "short_name_with_provider",
)
az_fields = (
    "region",
    "original_az_name",
    "az",
    "short_name",
    "short_name_with_provider",
)


### DRF
class CloudProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudProvider
        fields = provider_fields


class CloudRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudRegion
        fields = region_fields


class CloudAvailabilityZoneSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()

    class Meta:
        model = CloudAvailabilityZone
        fields = az_fields


### END DRF


def serialize_provider_region(provider) -> dict:
    return [
        {
            "provider": region.provider.provider,  # list provider first
            "original_region_name": region.original_region_name,
            "short_name": region.short_name,
            "short_name_with_provider": region.short_name_with_provider,
        }
        | {k: v for k, v in model_to_dict(region).items() if k in region_fields}
        for region in CloudRegion.objects.filter(provider=provider).order_by(
            "original_region_name"
        )
    ]


def serialize_regions() -> dict:
    regions = []
    for provider in CloudProvider.objects.values_list("provider", flat=True):
        regions += serialize_provider_region(provider)
    return regions


def serialize_provider_az(provider) -> dict:
    return [
        {
            "provider": provider,  # list provider first
            "original_az_name": az.original_az_name,
            "original_region_name": az.region.original_region_name,
            "short_name": az.short_name,
            "short_name_with_provider": az.short_name_with_provider,
        }
        | {
            k: v
            for k, v in model_to_dict(az).items()
            if k in az_fields and k != "region"
        }
        for az in CloudAvailabilityZone.objects.filter(
            region__provider__provider=provider
        ).order_by("original_az_name")
    ]


def serialize_azs() -> dict:
    azs = []
    for provider in CloudProvider.objects.values_list("provider", flat=True):
        azs += serialize_provider_az(provider)
    return azs

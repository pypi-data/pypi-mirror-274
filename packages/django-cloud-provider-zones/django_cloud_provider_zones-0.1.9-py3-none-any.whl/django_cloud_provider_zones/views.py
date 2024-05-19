from django.http import JsonResponse
from .models import CloudProvider, CloudRegion, CloudAvailabilityZone
from .serializers import (
    CloudProviderSerializer,
    CloudRegionSerializer,
    CloudAvailabilityZoneSerializer,
)


def cloud_provider_list_drf(request):
    cloud_providers = CloudProvider.objects.all()
    serializer = CloudProviderSerializer(cloud_providers, many=True)
    return JsonResponse(serializer.data, safe=False)


def cloud_region_list_drf(request):
    cloud_regions = CloudRegion.objects.all()
    serializer = CloudRegionSerializer(cloud_regions, many=True)
    return JsonResponse(serializer.data, safe=False)


def cloud_availability_zone_list_drf(request):
    cloud_availability_zones = CloudAvailabilityZone.objects.all()
    serializer = CloudAvailabilityZoneSerializer(cloud_availability_zones, many=True)
    return JsonResponse(serializer.data, safe=False)

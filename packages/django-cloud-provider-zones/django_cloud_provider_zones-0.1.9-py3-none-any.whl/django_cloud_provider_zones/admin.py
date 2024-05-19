from django.contrib import admin

from .models import CloudProvider, CloudRegion, CloudAvailabilityZone


class CloudRegionAdmin(admin.ModelAdmin):
    list_display = [
        "provider",
        "original_region_name",
        "short_name",
        "short_name_with_provider",
    ]
    list_filter = ["provider", "geographic_region", "cardinality"]
    search_fields = [
        "provider__provider",
        "original_region_name",
        "short_name_with_provider",
    ]
    show_facets = admin.ShowFacets.ALWAYS


class CloudAvailabilityZoneAdmin(admin.ModelAdmin):
    list_display = ["region", "az", "short_name", "short_name_with_provider"]
    list_filter = ["region__provider", "region__original_region_name"]
    show_facets = admin.ShowFacets.ALWAYS


admin.site.register(CloudProvider)
admin.site.register(CloudRegion, CloudRegionAdmin)
admin.site.register(CloudAvailabilityZone, CloudAvailabilityZoneAdmin)

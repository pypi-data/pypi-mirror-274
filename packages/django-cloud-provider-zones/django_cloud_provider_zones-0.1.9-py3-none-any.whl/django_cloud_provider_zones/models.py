from django.core import validators
from django.db import models

from .cloud_short_names import get_cardinality_short_name, get_region_short_name


class CloudProvider(models.Model):
    provider = models.CharField(
        max_length=4,
        unique=True,
        validators=[validators.MinLengthValidator(3)],
        primary_key=True,
    )

    def __str__(self):
        return self.provider.upper()

    class Meta:
        verbose_name = "Cloud Provider"


class CloudRegionManager(models.Manager):
    def get_by_natural_key(self, provider, original_region_name):
        return self.get(provider=provider, original_region_name=original_region_name)


class CloudRegion(models.Model):
    provider = models.ForeignKey(CloudProvider, on_delete=models.CASCADE)  # gcp
    geographic_region = models.CharField(
        max_length=32, validators=[validators.MinLengthValidator(2)]
    )  # europe
    cardinality = models.CharField(
        max_length=12, validators=[validators.MinLengthValidator(2)]
    )  # west
    number = models.CharField(max_length=4, blank=True, default="")  # 1
    original_region_name = models.CharField(
        max_length=64, db_index=True
    )  # europe-west1
    created = models.DateField(auto_now_add=True, editable=False)

    objects = CloudRegionManager()

    def natural_key(self):
        return (
            self.provider.pk,
            self.original_region_name,
        )

    natural_key.dependencies = ["django_cloud_provider_zones.cloudprovider"]

    @property
    def short_name(self):
        """europe-west1 -> euw1"""
        short_cardinality = get_cardinality_short_name(self.cardinality)
        short_geographic_region = get_region_short_name(self.geographic_region)
        return f"{short_geographic_region}{short_cardinality}{self.number}"

    @property
    def short_name_with_provider(self):
        """gcp europe-west1 -> gcpeuw1"""
        return f"{self.provider.provider}{self.short_name}"

    def __str__(self):
        return f"{self.provider.provider}-{self.original_region_name}"

    class Meta:
        ordering = ["provider", "original_region_name"]
        unique_together = ["provider", "original_region_name"]
        verbose_name = "Cloud Region"


class CloudAvailabilityZoneManager(models.Manager):
    def get_by_natural_key(self, az, region_natural_key):
        return self.get(
            az=az, region=CloudRegion.objects.get_by_natural_key(*region_natural_key)
        )


class CloudAvailabilityZone(models.Model):
    region = models.ForeignKey(CloudRegion, on_delete=models.CASCADE)
    original_az_name = models.CharField(max_length=64, db_index=True)
    az = models.CharField(max_length=4, validators=[validators.MinLengthValidator(1)])
    created = models.DateField(auto_now_add=True, editable=False)

    objects = CloudAvailabilityZoneManager()

    def natural_key(self):
        return (
            self.az,
            self.region.natural_key(),
        )

    natural_key.dependencies = ["django_cloud_provider_zones.cloudregion"]

    @property
    def short_name(self):
        return f"{self.region.short_name}z{self.az}"

    @property
    def short_name_with_provider(self):
        return f"{self.region.provider.provider}{self.short_name}"

    def __str__(self):
        return f"{self.region.provider.provider}-{self.original_az_name}"

    class Meta:
        ordering = ["region", "az"]
        verbose_name = "Cloud Availability Zone"
        unique_together = ["region", "az"]

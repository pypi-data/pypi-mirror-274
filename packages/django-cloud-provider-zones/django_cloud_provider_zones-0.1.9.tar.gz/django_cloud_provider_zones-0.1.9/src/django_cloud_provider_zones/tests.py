import json

from django.test import Client, TestCase
from django.test.utils import override_settings

from django_cloud_provider_zones import urls
from django_cloud_provider_zones.models import CloudProvider
from django_cloud_provider_zones.serializers import (
    serialize_provider_az,
    serialize_provider_region,
)


@override_settings(
    ROOT_URLCONF=urls,
    INSTALLED_APPS=[
        "django.contrib.contenttypes",
        "rest_framework",
        "django_cloud_provider_zones",
    ],
)
class CloudProviderTestCase(TestCase):
    fixtures = [
        "django_cloud_provider_zones-CloudProvider.json",
        "django_cloud_provider_zones-CloudRegion.json",
        "django_cloud_provider_zones-CloudAvailabilityZone.json",
    ]

    def setUp(self):
        self.client = Client()

    def test_cloud_provider_name(self):
        providers = [{"provider": "aws"}, {"provider": "gcp"}]
        r = self.client.get("/cloud-providers/")
        self.assertEqual(r.status_code, 200)
        response_dict = json.loads(r.content.decode("utf-8"))
        for provider in providers:
            self.assertIn(provider, response_dict)

    def test_region_fixture_data(self):
        """simple sanity check"""
        expected_regions = [
            {
                "provider": "gcp",
                "original_region_name": "us-west4",
                "geographic_region": "us",
                "cardinality": "west",
                "number": "4",
            },
            {
                "provider": "aws",
                "original_region_name": "ap-northeast-3",
                "geographic_region": "ap",
                "cardinality": "northeast",
                "number": "3",
            },
            {
                "provider": "azu",
                "original_region_name": "northcentralus",
                "geographic_region": "us",
                "cardinality": "northcentral",
                "number": "",
            },
        ]
        r = self.client.get("/cloud-regions/")
        self.assertEqual(r.status_code, 200)
        for test_region in expected_regions:
            results_count = 0
            for response in json.loads(r.content.decode("utf-8")):
                if test_region == {k: response[k] for k in test_region.keys()}:
                    results_count += 1
            self.assertEqual(results_count, 1)

    def test_availability_zone_fixture_data(self):
        expected_zones = [
            {
                "az": "a",
                "region": "gcp-us-west4",
            },
            {
                "az": "3",
                "region": "azu-koreacentral",
            },
        ]
        r = self.client.get("/cloud-availability-zones/")
        self.assertEqual(r.status_code, 200)
        for test_zone in expected_zones:
            results_count = 0
            for response in json.loads(r.content.decode("utf-8")):
                if test_zone == {k: response[k] for k in test_zone.keys()}:
                    results_count += 1
            self.assertEqual(results_count, 1)

    def test_short_name_with_provider_region_unique(self):
        r = self.client.get("/cloud-regions/")
        self.assertEqual(r.status_code, 200)
        regions = json.loads(r.content.decode("utf-8"))
        short_names = [region["short_name_with_provider"] for region in regions]
        self.assertGreater(len(short_names), 50)
        self.assertEqual(len(short_names), len(set(short_names)))

    def test_short_name_with_provider_az_unique(self):
        r = self.client.get("/cloud-availability-zones/")
        self.assertEqual(r.status_code, 200)
        zones = json.loads(r.content.decode("utf-8"))
        short_names = [zone["short_name_with_provider"] for zone in zones]
        self.assertGreater(len(short_names), 150)
        self.assertEqual(len(short_names), len(set(short_names)))

    def test_region_az_collisions_per_provider(self):
        """ensure all region and az 'short_name' are unique per provider"""
        for provider in CloudProvider.objects.values_list("provider", flat=True):
            regions = serialize_provider_region(provider)
            azs = serialize_provider_az(provider)
            region_short_names = set([region["short_name"] for region in regions])
            az_short_names = set([az["short_name"] for az in azs])
            self.assertFalse(region_short_names.intersection(az_short_names))

    def test_short_name_az_structure(self):
        r = self.client.get("/cloud-availability-zones/")
        self.assertEqual(r.status_code, 200)
        zones = json.loads(r.content.decode("utf-8"))
        for zone in zones:
            self.assertTrue(
                zone["short_name_with_provider"].endswith(zone["short_name"])
            )

    def test_short_name_region_structure(self):
        r = self.client.get("/cloud-regions/")
        self.assertEqual(r.status_code, 200)
        regions = json.loads(r.content.decode("utf-8"))
        for region in regions:
            self.assertTrue(
                region["short_name_with_provider"].endswith(region["short_name"])
            )

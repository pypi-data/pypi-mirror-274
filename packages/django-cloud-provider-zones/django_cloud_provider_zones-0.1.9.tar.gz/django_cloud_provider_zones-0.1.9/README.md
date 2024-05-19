https://pypi.org/project/django-cloud-provider-zones/

# Django Cloud Provider Regions
## Examples
For reference, and for use outside of Django, [region_data/normalized_azs.json](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/region_data/normalized_azs.json) and [region_data/normalized_regions.json](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/region_data/normalized_regions.json) contain all generated region and az names.

```json

```

## Why
This [Django app](https://docs.djangoproject.com/en/5.0/ref/applications/) provides a static list of region and availability zones for AWS (Amazon Web Services) and GCP (Google Cloud Platform) cloud providers.

The purpose of this app is to provide Cloud Provider Region/AZ lists easily available to Django apps. It provides stable, shortened, versions of names for provisioning  naming conventions.

The Regions/AZ list is currrent as of March 2024.

## Features
- Quick and easy access to cloud Region and AZs from other Django apps
- Provides shortened versions of Region and AZ names for use by provisioning tools
- DB primary key fields are stable, will not change as new Regions/AZs are added

## Installation

`pip install django-cloud-provider-zones`

Add to project's settings.py INSTALLED_APPS:
```
'rest_framework',
'django_cloud_provider_zones',
```

Optionally, include the DRF REST urls in your project's `urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
import django_cloud_provider_zones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cloudzones/', include('django_cloud_provider_zones.urls')),
]
```
Import model data

`./manage.py loaddata django_cloud_provider_zones-CloudProvider django_cloud_provider_zones-CloudRegion django_cloud_provider_zones-CloudAvailabilityZone`

If exposed via the Django admin, it is recommended that these App's models are "read only" so grant only View permissions.

### Models
[model diagram](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/django_models.png)

This app provides the following models:
- `CloudProvider`: Cloud provider names - currently `AWS` or `GCP` 
- `CloudRegion`: Cloud regions
- `CloudAvailabilityZone`: Availability zones within a region

Each region and AZ provides, as properties, short name versions with dashes removed. For example, `AWS us-east-1` has names
```
short_name: use1
short_name_with_provider: awsuse1
```

```
## CloudProvider ##
>>> CloudProvider.objects.values().first()
{'provider': 'aws'}

## CloudRegion ##
>>> CloudRegion.objects.values().first()
{'cardinality': 'northeast',
 'created': datetime.date(2024, 3, 27),
 'geographic_region': 'ap',
 'id': 11,
 'number': '1',
 'original_region_name': 'ap-northeast-1',
 'provider_id': 'aws'}

>>> CloudRegion.objects.first().short_name
'apne1'
>>> CloudRegion.objects.first().short_name_with_provider
'awsapne1'

## CloudAvailabilityZone ##
>>> CloudAvailabilityZone.objects.values().first()
{'az': 'a', 'created': datetime.date(2024, 3, 27), 'id': 27, 'region_id': 11}

>>> CloudAvailabilityZone.objects.first().short_name
'apne1a'
>>> CloudAvailabilityZone.objects.first().short_name_with_provider
'awsapne1a'
```

Regions and AZs use Django "natural keys" which allows filtering by the Provider's region name
```
## Region natural key ##
>>> CloudRegion.objects.first().natural_key()
('aws', 'ap-northeast-1')
>>> CloudRegion.objects.get_by_natural_key("aws", "us-east-1")
<CloudRegion: aws-us-east-1>

## AZ natural key ##
>>> CloudAvailabilityZone.objects.first().natural_key()
('a', ('aws', 'ap-northeast-1'))
>>> CloudAvailabilityZone.objects.get_by_natural_key('a', ('aws', 'ap-northeast-1'))
<CloudAvailabilityZone: aws-ap-northeast-1a>
```
### Exported JSON files
All generated names are exported to these files for reference
```
tasks/django_management_commands.py django_serialize_azs > region_data/normalized_azs.json
tasks/django_management_commands.py django_serialize_regions  > region_data/normalized_regions.json
```

### API Endpoints

Basic REST Get endpoints available see [urls.py](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/src/django_cloud_provider_zones/urls.py)

### Updating model data
To add a new provider, activate the poetry virtualenv with `poetry shell && poetry install`

Fetch raw json from the provider's API or cli tool, save it to [region_data/PROVIDER_unprocessed.json](https://github.com/yolabingo/django-cloud-provider-zones/tree/main/region_data) see AWS and GCP examples.
Create [tasks/format_json_PROVIDER](https://github.com/yolabingo/django-cloud-provider-zones/tree/main/tasks) which creates properly formatted json files
```
region_data/PROVIDER_provider.json
region_data/PROVIDER_region.json
region_data/PROVIDER_az.json
```
see AWS and GCP examples.

Add new provider `CLOUD_PROVIDERS` in `tasks/update_db_from_json.py` then run
```
tasks/django_management_commands.py django_makemigrations
tasks/django_management_commands.py django_migrate
tasks/django_management_commands.py django_update_fixture_from_json
```
Once that looks good add a couple simple tests to [src/django_cloud_provider_zones/tests.py](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/src/django_cloud_provider_zones/tests.py) then 

```tasks/django_management_commands.py django_test```

Bump version, commit and push as needed.

`poetry version patch && poetry publish`

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community and Django Software Foundation for Django
- Thanks to the maintainers of all dependencies on this project
- Thanks to Real Python for their [Installable Django App article](https://realpython.com/installable-django-app/)# django-cloud-provider-regions

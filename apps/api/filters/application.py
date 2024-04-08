import django_filters
from apps.organizations.models import Application
class ApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = Application
        fields = ['application_status']
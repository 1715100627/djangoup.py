import django_filters

from HttpTestcas.models import Interfaces


class InterfacesFilter(django_filters.rest_framework.FilterSet):
    """
    过滤
    """
    project = django_filters.CharFilter(field_name='project_id', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    url = django_filters.CharFilter(field_name='url', lookup_expr='icontains')

    class Meta:
        model = Interfaces
        fields = ['project', 'name', 'url']

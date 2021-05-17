import django_filters

from HttpTestcas.models import TestcaseReports


class Test_reportsFilter(django_filters.rest_framework.FilterSet):
    """
    过滤
    """
    version = django_filters.CharFilter(field_name='version', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    url = django_filters.CharFilter(field_name='url', lookup_expr='icontains')

    class Meta:
        model = TestcaseReports
        fields = ['version']

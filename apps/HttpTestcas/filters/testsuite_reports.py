import django_filters
from apps.HttpTestcas.models import TestsuiteReports


class TestsuiteReportsFilter(django_filters.rest_framework.FilterSet):
    """
    场景报告筛选
    """
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    name = django_filters.CharFilter(field_name='testsuite__name', lookup_expr='icontains')
    project = django_filters.CharFilter(field_name='testsuite__project_id', lookup_expr='exact')
    version = django_filters.CharFilter(field_name='version', lookup_expr='exact')

    class Meta:
        model = TestsuiteReports
        fields = ['status', 'version']

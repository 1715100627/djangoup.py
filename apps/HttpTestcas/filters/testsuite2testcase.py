# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         testsuite2testcase.py
# Description:  
# Author:       XiangjunZhao
# EMAIL:        2419352654@qq.com
# Date:         2019/11/26 9:14
# -------------------------------------------------------------------------------

import django_filters

from apps.HttpTestcas.models import Testsuite2Testcase


class Testsuite2TestcaseFilter(django_filters.rest_framework.FilterSet):
    """
    场景用例过滤
    """
    testsuite = django_filters.CharFilter(field_name='testsuite_id', lookup_expr='exact')

    class Meta:
        model = Testsuite2Testcase
        fields = ['testsuite']

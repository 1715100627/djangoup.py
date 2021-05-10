from django.http import StreamingHttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from testcase_reports.models import Reports
from testcase_reports.serializer import ReportsSerializer
from .filter import Test_reportsFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.utils.encoding import escape_uri_path
import re
import os
import json
from datetime import datetime
from django.conf import settings


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Reports.objects.filter(is_delete=False)
    serializer_class = ReportsSerializer
    # 过滤
    filter_class = Test_reportsFilter
    # filter_fields = ['id']
    # 指定权限类
    permission_classes = [permissions.IsAuthenticated]
    # 排序
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_fields = ['execute_time', 'version']
    ordering_fields = ['execute_time', 'version']

    def list(self, request, *args, **kwargs):
        response = super().list(self, request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": response.data,
            "message": "OK",
        })

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(self, request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": response.data,
            "message": "OK",
        })
from django.http import StreamingHttpResponse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from reports.models import Reports
from reports.serializer import ReportsSerializer
from .utils import format_output, get_file_contents
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
    # 指定过滤引擎
    # filter_fields = [DjangoFilterBackend]
    filter_fields = ['id', 'name']
    # 指定权限类
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # response.data['results'] = format_output(response.data['results'])
        return response

    @action(detail=True)
    def download(self, request, pk=None):
        instance = self.get_object()
        html = instance.html
        name = instance.name
        mtch = re.match('r(.*_)\d+', name)
        if mtch:
            mtch = mtch.group(1)
            report_filename = mtch + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
        else:
            report_filename = name

        # report_dir = os.path.join(settings.BASE_DIR, 'reports')
        report_path = os.path.join(settings.REPORTS_DIR, report_filename)
        with open(report_path, 'w+', encoding='utf-8') as one_file:
            one_file.write(html)

        response = StreamingHttpResponse(get_file_contents(report_path))
        report_path_final = escape_uri_path(report_filename)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename*=UTF-8""{}'.format(report_path_final)
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        datas = serializer.data
        try:
            datas['summary'] = json.loads(datas['summary'], encoding='utf-8')
        except Exception as e:
            pass
        return Response(datas)

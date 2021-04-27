from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from testcase_reports.utils import get_version
from testcases.models import Testcases
from testcases.serializer import TestcaseModeSerializer
import json
from rest_framework.views import APIView
import os
from django.conf import settings
from rest_framework.decorators import action
from utils.utils import get_paginated_response
from utils import handle_datas
from interfaces.models import Interfaces
from .testcases_task import batch_exec_testcase
from envs.models import Envs
from .http_dlient import HttpSession
from .testcase_debug import HttpTestcaseDebug


class TestcasesViewSet(viewsets.ModelViewSet):
    queryset = Testcases.objects.filter(is_delete=False)
    serializer_class = TestcaseModeSerializer
    # 指定过滤引擎
    # filter_fields = [DjangoFilterBackend]
    filter_fields = ['id', 'name']
    # 指定权限类
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": response.data},
            "message": "OK",
        })

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": response.data},
            "message": "OK",
        })

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": response.data},
            "message": "OK",
        })

    @action(['POST'], detail=False)
    def debug(self, request, *args, **kwargs):
        data = request.data
        env_id = data.get('env_id')
        testcase = data.get('testcase')
        name = testcase.get('name')
        api_id = testcase.get('api')
        headers = testcase.get('headers')
        request_data = testcase.get('request_data')
        request_data_type = testcase.get('request_data_type')
        expect_result = testcase.get('expect_result')

        api = Interfaces.objects.filter(id=api_id, is_delete=False).first()
        method = api.method

        env = Envs.objects.filter(id=env_id, is_delete=False).first()
        envs_url = env.base_url

        base_url = testcase.get('url')
        if base_url.startswith('http') or base_url.startswith('https'):
            pass
        else:
            base_url = envs_url + base_url

        http_session = HttpSession()

        http_debug = None
        if request_data_type == "Json":
            http_debug = HttpTestcaseDebug(http_session=http_session, name=name, url=base_url, method=method,
                                           headers=headers,
                                           request_data_type=request_data_type,
                                           json_data=request_data, expect_result=expect_result)
        elif request_data_type == "Form Data":
            http_debug = HttpTestcaseDebug(http_session=http_session, name=name, url=base_url, method=method,
                                           headers=headers,
                                           request_data_type=request_data_type,
                                           form_data=request_data, expect_result=expect_result)

        testcase_result = http_debug.debug()
        testcase_result.update({
            "api": api.id,
            "api_name": api.name,
            "testcase": testcase.get('id'),
            "testcase_name": testcase.get('name'),
            "request_data_type": request_data_type,
            'is_periodictask': False
        })
        return Response({
            "code": 200,
            "data": {"data": testcase_result},
            "message": "OK",
        })


class TestcaseBatchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        testcases = data.get('testcases')
        version = get_version()

        # 异步执行
        batch_exec_testcase(testcases=testcases, version=version)

        return Response({
            "code": 200,
            "data": '程序正在后台运行中,请稍后查看结果……',
            "message": "OK",
        })


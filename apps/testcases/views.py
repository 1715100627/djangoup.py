from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from testcases.models import Testcases
from testcases.serializer import TestcaseModeSerializer, TestcaseRunSerializer, ReadsSerializer
import json
from datetime import datetime
import os
from django.conf import settings
from rest_framework.decorators import action
from utils.utils import get_paginated_response
from utils import handle_datas
from interfaces.models import Interfaces
from configures.models import Configures
from envs.models import Envs
from httprunner import HttpRunner
from utils import common


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

    # 搜索
    @action(methods=['post'], detail=False)
    def reads(self, request, *args, **kwargs):

        names = request.data.get('data')  # 获取参数

        if names is not '':
            # __contains模糊查询
            queryset = Testcases.objects.filter(name__contains=names)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ReadsSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

    def retrieve(self, request, *args, **kwargs):
        testcase_obj = self.get_object()

        # 前置信息
        testcase_include = json.loads(testcase_obj.include)

        # 请求信息
        testcase_request = json.loads(testcase_obj.request)
        testcase_request_datas = testcase_request.get('test').get('request')

        # validate断言
        testcase_validate = testcase_request.get('test').get('validate')
        testcase_validate_list = handle_datas.handle_data3(testcase_validate)

        # 处理用例param数据，查询字符串参数
        testcase_param = testcase_request_datas.get('param')
        testcase_param_list = handle_datas.handle_data1(testcase_param)

        # 处理header请求头
        testcase_headers = testcase_request_datas.get('headers')
        testcase_headers_list = handle_datas.handle_data1(testcase_headers)

        # 处理用例variables全局
        testcase_variables = testcase_request.get('test').get('variables')
        testcase_variables_list = handle_datas.handle_data2(testcase_variables)

        # 处理form表单数据
        testcase_from_dasts = testcase_request_datas.get('data')
        testcase_from_dasts_list = handle_datas.handle_data4(testcase_from_dasts)

        # 处理json数据
        testcase_json_datas = json.dumps(testcase_request_datas.get('json'), ensure_ascii=False)

        # 处理extract数据，提取token
        testcase_extract_datas = testcase_request.get('test').get('extract')
        testcase_extract_datas_list = handle_datas.handle_data5(testcase_extract_datas)

        # 处理paramets数据，参数化
        testcase_parameters_datas = testcase_request.get('test').get('parameters')
        testcase_parameters_datas_list = handle_datas.handle_data5(testcase_parameters_datas)

        # 处理setupHooks数据前置
        testcase_setup_hooks_datas = testcase_request.get('test').get('setup_hooke')
        testcase_setup_hooks_datas_list = handle_datas.handle_data6(testcase_setup_hooks_datas)

        # 处理teardownHooks数据
        testcase_teardown_hooks_datas = testcase_request.get('test').get('teardown_hooks')
        testcase_teardown_hooks_datas_list = handle_datas.handle_data6(testcase_teardown_hooks_datas)

        selected_configure_id = testcase_include.get('config')
        selected_interface_id = testcase_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id
        selected_testcase_id = testcase_include.get('testcase')

        datas = {
            'author': testcase_obj.author,
            'testcase_name': testcase_obj.name,
            'selected_configure_id': selected_configure_id,
            'selected_interface_id': selected_interface_id,
            'selected_project_id': selected_project_id,
            'selected_testcase_id': selected_testcase_id,

            'method': testcase_request_datas.get('method'),
            'url': testcase_request_datas.get('url'),
            'param': testcase_param_list,
            'header': testcase_headers_list,
            'variable': testcase_from_dasts_list,  # form表单数据
            'jsonVariable': testcase_json_datas,

            'extract': testcase_extract_datas_list,
            'validate': testcase_validate_list,
            'globalVar': testcase_variables_list,
            'parameterized': testcase_parameters_datas_list,
            'setupHooks': testcase_setup_hooks_datas_list,
            'teardownHooks': testcase_teardown_hooks_datas_list,

        }
        return Response(datas)

    @action(detail=True)
    def configs(self, request, pk=None):
        configs_objs = Configures.objects.filter(interface_id=pk, is_delete=False)
        one_list = []
        for obj in configs_objs:
            one_list.append({
                'id': obj.id,
                'name': obj.name
            })
        return Response(data=one_list)

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid()
        datas = serializer.validated_data

        env_id = datas.get('env_id')
        testcase_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        os.mkdir(testcase_path)
        # first()返回queryset查询集第一项
        env = Envs.objects.filter(id=env_id, is_delete=False).first()

        # 生成yml文件
        common.generate_testcase_files(instance, env, testcase_path)
        # 运行用例
        return common.run_testcase(instance, testcase_path)

    def get_serializer_class(self):
        if self.action == 'run':
            return TestcaseRunSerializer
        else:
            return TestcaseModeSerializer

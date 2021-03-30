import os
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from envs.models import Envs
from .utils import get_testcases_by_interface_ids
from testcases.models import Testcases
from testsuits.models import Testsuits
from testsuits.serializer import TestSuitsModeSerializer, ReadsSerializer
from utils import common
from utils.utils import get_paginated_response_update, get_paginated_response
from .serializer import TestsuitsRunSerializer


class TestSuitsViewSet(viewsets.ModelViewSet):
    queryset = Testsuits.objects.filter(is_delete=False)
    serializer_class = TestSuitsModeSerializer
    # 指定过滤引擎
    # filter_fields = [DjangoFilterBackend]
    filter_fields = ['id', 'name', 'project']
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

    # 搜索
    @action(methods=['post'], detail=False)
    def reads(self, request, *args, **kwargs):

        names = request.data.get('data')  # 获取参数

        if names is not '':
            # __contains模糊查询
            queryset = Testsuits.objects.filter(name__contains=names)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ReadsSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response['results'] = get_paginated_response_update(response.data['data']['data'])
        response['results'] = get_paginated_response(response.data['data']['data'])
        return response

    @action(methods=['post'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid()
        datas = serializer.validated_data

        env_id = datas.get('env_id')
        testcase_dir_path = os.path.join(settings.SUITES_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f'))
        if not os.path.exists(testcase_dir_path):
            os.mkdir(testcase_dir_path)

        # first()返回queryset查询集第一项
        env = Envs.objects.filter(id=env_id, is_delete=False).first()

        include = eval(instance.include)

        if len(include) == 0:
            data_dict = {
                'detail': '此套件下未添加用例，无法运行'
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        # 将include中的接口id转换为此接口下的id
        include = get_testcases_by_interface_ids(include)

        for testcase_id in include:
            testcase_objs = Testcases.objects.filter(is_delete=False, id=testcase_id).first()

            if testcase_objs:
                # 生成yml文件
                common.generate_testcase_files(testcase_objs, env, testcase_dir_path)

        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return TestsuitsRunSerializer if self.action == 'run' else self.serializer_class

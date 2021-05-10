from datetime import datetime
import os

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import permissions

from HttpTestcas.models import Envs
from HttpTestcas.models import Interfaces
from HttpTestcas.serializers import InterfacesModeSerializer, InterfacesRunSerializer, inReadsSerializer,CreateMOdelSerializer
from rest_framework.decorators import action

from HttpTestcas.filters import InterfacesFilter
from utils import common
from utils.utils import get_paginated_response, get_paginated_response_create
from HttpTestcas.models import Testcases
# from configures.models import Configures
from django.conf import settings


class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.filter(is_delete=False)
    filter_class = InterfacesFilter
    serializer_class = InterfacesModeSerializer
    # 指定过滤引擎
    # filter_fields = [DjangoFilterBackend]
    filter_fields = ['id', 'name']
    # 指定权限类
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除

    # 自定义删除返回信息
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": "删除成功",
            "message": "OK",
        })


    # def create(self, request, *args, **kwargs):
    #     super().create(request, *args, **kwargs)
    #     return Response({
    #         "code": 200,
    #         "data": {"data": request.data},
    #         "message": "OK",
    #     })

    # 搜索
    @action(methods=['post'], detail=False)
    def reads(self, request, *args, **kwargs):

        project = request.data.get('project')
        name = request.data.get('name')
        url = request.data.get('url')

        if project is not '':
            # __contains模糊查询
            queryset = Interfaces.objects.filter(project=project)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = InterfacesModeSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            datas = serializer.data
            datas = get_paginated_response(datas)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True)
    # def configs(self, request, pk=None):
    #     configs_objs = Configures.objects.filter(interface_id=pk, is_delete=False)
    #     one_list = []
    #     for obj in configs_objs:
    #         one_list.append({
    #             'id': obj.id,
    #             'name': obj.name
    #         })
    #     # return Response(data=one_list)
    #     return Response({
    #         "code": 200,
    #         "data": {"data": one_list},
    #         "message": "OK",
    #     })


    @action(detail=True)
    def testcases(self, request, pk=None):
        testcases_objs = Testcases.objects.filter(interface_id=pk, is_delete=False)
        one_list = []
        for obj in testcases_objs:
            one_list.append({
                'id': obj.id,
                'name': obj.name
            })
        # return Response(data=one_list)
        return Response({
            "code": 200,
            "data": {"data": one_list},
            "message": "OK",
        })

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
        # 项目下所有接口
        testcase_objs = Testcases.objects.filter(is_delete=False, interface=instance)

        if not testcase_objs.exists():
            data_dict = {
                'detail': '此接口下没有用例，无法运行'
            }
            return Response(data_dict, status=status.HTTP_400_BAD_REQUEST)

        for one_obj in testcase_objs:
            common.generate_testcase_files(one_obj, env, testcase_dir_path)

        # 运行用例
        return common.run_testcase(instance, testcase_dir_path)

    def get_serializer_class(self):
        return InterfacesRunSerializer if self.action == 'run' else self.serializer_class


class CreateModelViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.filter(is_delete=False)
    serializer_class = CreateMOdelSerializer

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": request.data},
            "message": "OK",
        })

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": request.data},
            "message": "OK",
        })
import json

from rest_framework.decorators import action
from rest_framework.response import Response
from utils import handle_datas
from rest_framework.viewsets import ModelViewSet
from .models import Configures
from .serializer import ConfiguresSerializer, ReadsSerializer
from rest_framework import permissions
from interfaces.models import Interfaces


class ConfiguresViewSet(ModelViewSet):
    queryset = Configures.objects.filter(is_delete=False)
    serializer_class = ConfiguresSerializer
    filter_fields = ['id', 'name']
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

    def create(self, request, *args, **kwargs):
        # super().create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

    def retrieve(self, request, *args, **kwargs):
        config_obj = self.get_object()
        config_request = json.loads(config_obj.request, encoding='utf-8')

        # json转为嵌套字典列表
        config_headers = config_request['config']['request'].get('headers')
        config_headers_list = handle_datas.handle_data1(config_headers)

        # 全局变量转嵌套字典列表
        config_variables = config_request['config'].get('variables')
        config_variables_list = handle_datas.handle_data2(config_variables)

        config_name = config_request['config']['name']
        selected_interface_id = config_obj.interface_id
        selected_project_id = Interfaces.objects.get(id=selected_interface_id).project_id

        datas = {
            'author': config_obj.author,
            'configure_name': config_name,
            'selected_interface_id': selected_interface_id,
            'selected_project_id': selected_project_id,
            'header': config_headers_list,
            'globalVar': config_variables_list
        }
        return Response({
            "code": 200,
            "data": {"data": datas},
            "message": "OK",
        })

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": request.data},
            "message": "OK",
        })

    # 搜索
    @action(methods=['post'], detail=False)
    def reads(self, request, *args, **kwargs):

        names = request.data.get('data')  # 获取参数

        if names is not '':
            # __contains模糊查询
            queryset = Configures.objects.filter(name__contains=names)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ReadsSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

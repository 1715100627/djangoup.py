import json

from rest_framework.response import Response
from utils import handle_datas
from rest_framework.viewsets import ModelViewSet
from .models import Configures
from .serializer import ConfiguresSerializer
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
        return Response(datas)

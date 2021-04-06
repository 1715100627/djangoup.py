from rest_framework.decorators import action
from rest_framework.response import Response

from module.models import Module
from rest_framework import viewsets, status
from module.serializer import ModuleModeSerializer,ModuleFindModeSerializer


class ModularViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.filter(is_delete=False)
    serializer_class = ModuleModeSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    @action(methods=['post'], detail=True)
    def findmodule(self, request, *args, **kwargs):

        id = request.data.get('projectId')  # 获取参数

        if id is not '':
            # __contains模糊查询
            queryset = Module.objects.filter(project=id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ModuleFindModeSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })
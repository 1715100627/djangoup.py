from rest_framework.decorators import action
from rest_framework.response import Response

from HttpTestcas.models import Projects
from HttpTestcas.models import Module
from rest_framework import viewsets, status
from HttpTestcas.serializers import ModuleModeSerializer, ModuleFindModeSerializer, ModuleCreadModeSerializer, \
    ModuleListModeSerializer


class ModularViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.filter(is_delete=False)
    serializer_class = ModuleListModeSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

    # def create(self, request, *args, **kwargs):
    #     response = super().create(request, *args, **kwargs)
    #     return Response({
    #         "code": 200,
    #         "data": {"data": response.data},
    #         "message": "OK",
    #     })

    @action(methods=['post'], detail=True)
    def findmodule(self, request, *args, **kwargs):

        id = request.data.get('projectId')  # 获取参数

        if id is not '':
            # __contains模糊查询
            queryset = Module.objects.filter(project=id)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ModuleCreadModeSerializer(queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })

    @action(methods=['GET'], detail=True)
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ModuleFindModeSerializer(instance=queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })


class CreateModularViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.filter(is_delete=False)
    serializer_class = ModuleCreadModeSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        parent = data.get('parent')
        if parent:
            parent_module = Module.objects.filter(id=parent, is_delete=False).first()
            if parent_module.floor == 4:
                return Response({
                    "code": 200,
                    "data": '模块创建失败，原因：模块层级最多为4层',
                    "message": "OK",
                })
            else:
                data['floor'] = parent_module.floor + 1
        else:
            data['floor'] = 1

        response = super().create(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": response.data},
            "message": "OK",
        })

    def update(self, request, *args, **kwargs):
        # project = Projects.objects.filter(id=request.data.get('project')).filter()
        # requests = request.data.pop('project')
        # request.data['project'] = project
        response = super().update(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {"data": response.data},
            "message": "OK",
        })

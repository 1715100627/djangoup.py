from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from envs.models import Envs
from envs.serializer import EnvModeSerializer, ReadsSerializer
from rest_framework.decorators import action

from utils.utils import get_paginated_response,get_paginated_response_create


class EnvsViewSet(viewsets.ModelViewSet):
    queryset = Envs.objects.filter(is_delete=False)
    serializer_class = EnvModeSerializer
    # 指定过滤引擎
    # filter_fields = [DjangoFilterBackend]
    filter_fields = ['id', 'name']
    # 指定权限类
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        instance.is_delete = True
        instance.save()  # 逻辑删除

    # 自定义增加返回信息
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {'data': request.data},
            "message": "OK",
        })

    # 自定义删除返回信息
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": "删除成功",
            "message": "OK",
        })

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        #
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     datas = serializer.data
        #     datas = get_paginated_response(datas)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

        response = super().list(request, *args, **kwargs)
        response['results'] = get_paginated_response(response.data['data']['data'])
        return response

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        datas = request.data
        return Response({
            "code": 200,
            "data": {"data": datas},
            "message": "OK",
        })


    @action(methods=['get'], detail=False)
    def names(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response({
            "code": 200,
            "data": {"data": serializer.data},
            "message": "OK",
        })
        # return Response(serializer.data)

    # 搜索
    @action(methods=['post'], detail=False)
    def reads(self, request, *args, **kwargs):

        names = request.data.get('data')  # 获取参数

        if names is not '':
            # __contains模糊查询
            queryset = Envs.objects.filter(name__contains=names)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        serializer = ReadsSerializer(queryset, many=True)
        serializer = get_paginated_response_create(serializer.data)
        return Response({
            "code": 200,
            "data": {"data": serializer},
            "message": "OK",
        })
from HttpTestcas.models import Testsuite
from HttpTestcas.serializers.testsuite import TestSuiteSerializer, TestCreatsuiteSerializer
from HttpTestcas.core.utils import get_version
from HttpTestcas.tasks.testsuite_task import batch_exec_testsuite

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView


class TestsuiteList(viewsets.ModelViewSet):
    queryset = Testsuite.objects.filter(is_delete=False)
    serializer_class = TestSuiteSerializer
    filter_fields = ['id', 'name']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(response.data)


class TestsuiteViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    '创建、更新'
    queryset = Testsuite.objects.filter(is_delete=False)
    serializer_class = TestCreatsuiteSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": response.data,
            "message": "OK",
        })


class TestsuiteBatchAPIView(APIView):
    def post(self, request, *args, **kwargs):
        pass
        data = request.data
        testsuites = data.get('testsuites')
        version = get_version()
        batch_exec_testsuite(testsuites=testsuites, version=version)
        return Response({
            "code": 200,
            "data": '程序正在后台运行中,请稍后查看结果……',
            "message": "OK",
        })

from rest_framework import viewsets
from .models import Testsuite
from .serializer import TestSuiteSerializer, TestCreatsuiteSerializer
from rest_framework import permissions
from rest_framework.response import Response

from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


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
        response = super().create(request,*args,**kwargs)
        return Response({
            "code": 200,
            "data": response.data,
            "message": "OK",
        })
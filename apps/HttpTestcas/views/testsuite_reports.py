from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from HttpTestcas.models import TestsuiteReports
from HttpTestcas.serializers import TestsuiteReportsSerializer
from HttpTestcas.filters import TestsuiteReportsFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class TestsuiteReportsViewSet(viewsets.ModelViewSet):
    queryset = TestsuiteReports.objects.filter(is_delete=False)
    serializer_class = TestsuiteReportsSerializer

    filter_class = TestsuiteReportsFilter

    # 权限
    permission_classes = [permissions.IsAuthenticated]

    # 排序
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filter_fields = ['execute_time', 'version']
    # ordering_fields = ['execute_time', 'version']

    def retrieve(self,request,*args,**kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "code": 200,
            "data": {'data': response.data},
            "message": "OK",
        })


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response

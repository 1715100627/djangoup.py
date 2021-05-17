from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from HttpTestcas.models import Testsuite2Testcase, Testcases
from HttpTestcas.filters.testsuite2testcase import Testsuite2TestcaseFilter
from HttpTestcas.serializers import Testsuite2TestcaseSerializer


class Testsuite2TestcaseViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Testsuite2Testcase.objects.filter(is_delete=False)
    serializer_class = Testsuite2TestcaseSerializer
    filter_class = Testsuite2TestcaseFilter

    def create(self, request, *args, **kwargs):
        testsuite2testcase = request.data
        testsuite_id = testsuite2testcase.get('testsuite_id')
        data = testsuite2testcase.get('data') if testsuite2testcase else None

        Testsuite2Testcase.objects.filter(testsuite_id=testsuite_id).delete()
        testsuite2testcase = []

        for item in data:
            testsuite2testcase.append(Testsuite2Testcase(**item))
        Testsuite2Testcase.objects.bulk_create(testsuite2testcase)
        return Response({
            "code": 200,
            "data": '',
            "message": "OK",
        })
from rest_framework.serializers import ModelSerializer
from HttpTestcas.models import Projects
from HttpTestcas.models import Interfaces
from HttpTestcas.models import Testcases
from HttpTestcas.models import Testsuite2Testcase


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'is_delete')


class ApiSerializer(ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'is_delete','project')


class TestcaseSerializer(ModelSerializer):
    api = ApiSerializer()

    class Meta:
        model = Testcases
        fields = "__all__"

class Testsuite2TestcaseSerializer(ModelSerializer):
    testcase = TestcaseSerializer()

    class Meta:
        model = Testsuite2Testcase
        exclude = ('id',)

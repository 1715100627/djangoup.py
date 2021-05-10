from rest_framework import serializers
from HttpTestcas.models import Testsuite
from HttpTestcas.serializers.project import ProjectModuleSerializer
from HttpTestcas.models import Testcases


# class TestcaseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Testcases
#         fields = ('id', 'name', 'is_delete')


class TestSuiteSerializer(serializers.ModelSerializer):
    project = ProjectModuleSerializer()
    testcases = serializers.SerializerMethodField()

    def get_testcases(self, obj):
        result = obj.testcases.values('id', 'name', 'is_delete')
        return result

    class Meta:
        model = Testsuite
        fields = '__all__'


class TestCreatsuiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testsuite
        exclude = ('status','testcases')
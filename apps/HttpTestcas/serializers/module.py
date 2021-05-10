from rest_framework import serializers
from HttpTestcas.models import Module
from HttpTestcas.models import Projects
from rest_framework.response import Response
from HttpTestcas.serializers.project import ProjectModuleSerializer


class ModuleModeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(read_only=True)
    project = ProjectModuleSerializer()

    # project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), help_text='项目ID')

    class Meta:
        model = Module
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True}
        }


class ModuleFindModeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'name', 'parent', 'floor', 'project', 'desc', 'tester')


class ModuleCreadModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


class ModuleListModeSerializer(serializers.ModelSerializer):
    project = ProjectModuleSerializer()

    class Meta:
        model = Module
        fields = '__all__'
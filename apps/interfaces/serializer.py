from rest_framework import serializers
from interfaces.models import Interfaces
from projects.models import Projects
from module.models import Module
from rest_framework.response import Response


class ProjectModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'is_delete')


class ModuleModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'is_delete')


class InterfacesModeSerializer(serializers.ModelSerializer):
    # project = serializers.StringRelatedField(help_text='项目名称')
    # PrimaryKeyRelatedField 前端传id，自动转换为模型类对象
    # project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), help_text='项目ID')
    project = ProjectModeSerializer()
    module = ModuleModeSerializer()

    class Meta:
        model = Interfaces
        fields = '__all__'
        # exclude = ('update_time', 'is_delete')
        # read_only_fields = ('leader', 'tester')
        # extra_kwarge = {
        #     'create_time': {
        #         "read_only": True
        #     },
        # }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        interface = Interfaces.objects.create(**validated_data)
        return interface

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project = validated_data.pop('project_id')
            validated_data['project'] = project
        instance = super().update(instance, validated_data)
        return instance


class InterfacesRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境变量ID", write_only=True)

    class Meta:
        model = Interfaces
        fields = ('id', 'env_id')


class inReadsSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'project', 'tester', 'desc')

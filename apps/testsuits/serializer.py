from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from utils.base_models import BaseModel
from testsuits.models import Testsuits
from debugtalks.models import Debugtalks
from interfaces.models import Interfaces
from projects.models import Projects


class TestSuitsModeSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')
    # PrimaryKeyRelatedField 前端传id，自动转换为模型类对象
    project_id = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all(), help_text='项目ID')

    class Meta:
        model = Testsuits
        fields = ('id', 'name', 'project', 'project_id', 'include', 'create_time', 'update_time')
        extra_kwarge = {
            'create_time': {
                "read_only": True
            },
            'update_time': {
                'read_only': True
            },
            'include': {
                'write_only': True
            },
        }

    def create(self, validated_data):
        project = validated_data.pop('project_id')
        validated_data['project'] = project
        testsuit = Testsuits.objects.create(**validated_data)
        return testsuit

    def update(self, instance, validated_data):
        if 'project_id' in validated_data:
            project_obj = validated_data.pop('project_id')
            validated_data['project'] = project_obj

        return super().update(instance, validated_data)

class TestsuitsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境变量ID", write_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'env_id')
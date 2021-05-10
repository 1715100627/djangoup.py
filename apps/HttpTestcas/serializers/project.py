from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from HttpTestcas.models import Projects
from HttpTestcas.models import Envs
from HttpTestcas.models import Interfaces


class EnvsModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        fields = '__all__'


class ProjectModeSerializer(serializers.ModelSerializer):
    envs = EnvsModeSerializer(many=True)

    class Meta:
        model = Projects
        fields = '__all__'


class ProjectCreModeserializer(serializers.ModelSerializer):

    def create(self, validated_data):
        project_obj = super().create(validated_data)
        return project_obj

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = Projects
        fields = '__all__'


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境变量ID", write_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'env_id')


class ProjectModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'is_delete')

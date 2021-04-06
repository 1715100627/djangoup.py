from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from projects.models import Projects
from debugtalks.models import Debugtalks
from envs.models import Envs
from interfaces.models import Interfaces


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
        Debugtalks.objects.create(project=project_obj)
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



# class InterfacesNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Interfaces
#         fields = ('id', 'name', 'tester')
#
#
# class InterfacesByProjectIdSerializer(serializers.ModelSerializer):
#     interfaces_set = InterfacesNameSerializer(read_only=True, many=True)

# class Meta:
#     model = Projects
#     fields = ('id', 'interfaces_set')


class ProjectsRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境变量ID", write_only=True)

    class Meta:
        model = Projects
        fields = ('id', 'env_id')

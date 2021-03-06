from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from projects.models import Projects
from debugtalks.models import Debugtalks
from interfaces.models import Interfaces


class ProjectModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        # filter=('id','name','leader','tester')
        # filter = '__all__'
        exclude = ('update_time', 'is_delete')
        # read_only_fields = ('leader', 'tester')
        extra_kwarge = {
            'create_time': {
                "read_only": True
            },
        }

    def create(self, validated_data):
        project_obj = super().create(validated_data)
        Debugtalks.objects.create(project=project_obj)
        return project_obj


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


class ReadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'leader', 'tester', 'programmer', 'publish_app', 'desc')


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

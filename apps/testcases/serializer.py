from rest_framework import serializers
from testcases.models import Testcases
from projects.models import Projects
from interfaces.models import Interfaces
import json


class IntercfacesAnotherSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')
    pid = serializers.IntegerField(write_only=True, help_text='项目ID')
    iid = serializers.IntegerField(write_only=True, help_text='接口ID')

    class Meta:
        model = Interfaces
        fields = ('iid', 'name', 'project', 'pid')

        extra_kwargs = {
            'name': {
                'read_only': True  # 只输出
            }
        }


class TestcaseModeSerializer(serializers.ModelSerializer):
    interface = IntercfacesAnotherSerializer(help_text='项目ID和接口ID')

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'interface', 'include', 'author', 'request')
        extra_kwarge = {
            'include': {
                "write_only": True
            },
            'request': {
                "write_only": True
            }
        }

    def create(self, validated_data):
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['iid']
        return Testcases.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'interface' in validated_data:
            interface_dict = validated_data.pop('interface')
            validated_data['interface_id'] = interface_dict['iid']
        return super().update(instance, validated_data)


class TestcaseRunSerializer(serializers.ModelSerializer):
    env_id = serializers.IntegerField(help_text="环境变量ID", write_only=True)

    class Meta:
        model = Testcases
        fields = ('id', 'env_id')


class ReadsSerializer(serializers.ModelSerializer):
    interface = IntercfacesAnotherSerializer(help_text='项目ID和接口ID')

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'author', 'interface')

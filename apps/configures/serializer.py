from rest_framework import serializers
from .models import Configures
from interfaces.models import Interfaces


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


class ConfiguresSerializer(serializers.ModelSerializer):
    interface = IntercfacesAnotherSerializer(help_text='项目ID和接口ID')

    class Meta:
        model = Configures
        fields = ('id', 'name', 'interface', 'author', 'request')
        extra_kwargs = {
            'request': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        interface_dict = validated_data.pop('interface')
        validated_data['interface_id'] = interface_dict['iid']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'interface' in validated_data:
            interface_dict = validated_data.pop('interface')
            validated_data['interface_id'] = interface_dict['iid']
        return super().update(instance, validated_data)


class ReadsSerializer(serializers.ModelSerializer):
    interface = IntercfacesAnotherSerializer(help_text='项目ID和接口ID')

    class Meta:
        model = Configures
        fields = ('id', 'name', 'author', 'interface')
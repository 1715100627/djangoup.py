from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from HttpTestcas.models import Envs
# from debugtalks.models import Debugtalks
from HttpTestcas.models import Interfaces


class EnvModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        # filter=('id','name','leader','tester')
        # filter = '__all__'
        exclude = ('update_time', 'is_delete')
        # read_only_fields = ('leader', 'tester')
        extra_kwarge = {
            'create_time': {
                "read_only": True
            },
        }


class ReadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Envs
        fields = ('id', 'name', 'base_url', 'desc', 'create_time','is_active')

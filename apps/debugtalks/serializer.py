from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from debugtalks.models import Debugtalks
from debugtalks.models import Debugtalks
from interfaces.models import Interfaces


class DebugtalksModeSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(help_text='项目名称')

    class Meta:
        model = Debugtalks
        # filter=('id','name','leader','tester')
        # filter = '__all__'
        exclude = ('update_time', 'is_delete', 'create_time')
        # read_only_fields = ('leader', 'tester')
        extra_kwarge = {
            'debugtalk': {
                "write_only": True
            },
        }
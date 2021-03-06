from rest_framework import serializers
from .models import Reports


class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        exclude = ('update_time', 'is_delete')

        extra_lwarge = {
            'html': {
                'write_only': True
            },
            'create_time': {
                'read_only': True
            }
        }

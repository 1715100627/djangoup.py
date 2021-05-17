from rest_framework import serializers
from HttpTestcas.models import TestsuiteReports


class TestsuiteReportsSerializer(serializers.ModelSerializer):
    execute_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = TestsuiteReports
        fields = '__all__'

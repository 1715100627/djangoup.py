from rest_framework import serializers
from HttpTestcas.models import Reports


class ReportsSerializer(serializers.ModelSerializer):
    execute_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Reports
        fields = '__all__'

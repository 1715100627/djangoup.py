from rest_framework import serializers
from module.models import Module
from projects.models import Projects
from rest_framework.response import Response


class ModuleModeSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(read_only=True)
    project = serializers.CharField(read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'name', 'parent', 'floor', 'project','desc','tester')
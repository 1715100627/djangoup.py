from rest_framework import serializers
from rest_framework.response import Response

from testcases.models import Testcases
from projects.models import Projects
from interfaces.models import Interfaces
import json


class TestcaseModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testcases
        fields = '__all__'


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'is_deleted')


class ApiNameSerializer(serializers.ModelSerializer):
    project = ProjectNameSerializer()

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'url', 'project', 'is_deleted')


class TestcaseListSerializer(serializers.ModelSerializer):
    api = ApiNameSerializer()

    class Meta:
        model = Testcases
        fields = '__all__'

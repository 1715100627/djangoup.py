from rest_framework import serializers
from rest_framework.response import Response

from HttpTestcas.models import Testcases
from HttpTestcas.models import Projects
from HttpTestcas.models import Interfaces
import json


class TestcaseModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testcases
        fields = '__all__'


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name', 'is_delete')


class ApiNameSerializer(serializers.ModelSerializer):
    project = ProjectNameSerializer()

    class Meta:
        model = Interfaces
        fields = ('id', 'name', 'url', 'project', 'is_delete')


class TestcaseListSerializer(serializers.ModelSerializer):
    api = ApiNameSerializer()

    class Meta:
        model = Testcases
        fields = '__all__'

from module.models import Module
from rest_framework import viewsets, status
from module.serializer import ModuleModeSerializer


class ModularViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.filter(is_delete=False)
    serializer_class = ModuleModeSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from djangoProject.celery import app as celery_app


# 获取已注册的celery任务
class TasksAPIView(GenericAPIView):
    pagination_class = None

    def get(self, request, *args, **kwargs):
        tasks = list(sorted(name for name in celery_app.tasks if not name.startswith('celery.')))
        return Response(tasks)
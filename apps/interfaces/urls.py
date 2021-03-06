# from .views import index
from django.urls import path, include
from interfaces import views
from rest_framework import routers

# 创建路由对象
# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# 注册路由
# 1.路由前缀 2.视图集
router.register(r'interfaces', views.InterfacesViewSet)
urlpatterns = [
]
urlpatterns += router.urls

# urlpatterns = [
#     # path('', views.IndexView.as_view())
#     path('projects/', views.ProjectsViewSet.as_view({
#         'get': 'list',
#         'post': 'create'
#     }),name='projects-list'),
#
#     path('projects/<int:pk>/', views.ProjectsViewSet.as_view({
#         'get': 'retrieve',
#         'put': 'update',
#         'delete': 'destroy'
#     })),
#
#     path('projects/names/', views.ProjectsViewSet.as_view({
#         'get': 'names',
#     }),name='project-names'),
#
#     path('projects/<int:pk>/interfaces/', views.ProjectsViewSet.as_view({
#         'get': 'interfaces',
# }))
# ]

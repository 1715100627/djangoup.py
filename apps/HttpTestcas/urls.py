# from .views import index
from django.urls import path, include
from apps.HttpTestcas.views import *
from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

# 创建路由对象
# router = routers.SimpleRouter()
router = routers.DefaultRouter()
# 注册路由
# 1.路由前缀 2.视图集
router.register(r'projects', ProjectsViewSet)
router.register(r'projadd', ProjectsAddViewSet)
router.register(r'envs', EnvsViewSet)
router.register(r'interfaces', InterfacesViewSet)
router.register(r'interfaadd', CreateModelViewSet)
router.register(r'module', ModularViewSet)
router.register(r'moduleadd', CreateModularViewSet)
router.register(r'testcase_reports', ReportViewSet)
router.register(r'testcases', TestcasesViewSet)
router.register(r'testcaseslist', TestcaseListViewSet)
router.register(r'testsuite', TestsuiteList)
router.register(r'testsuitec', TestsuiteViewSet)
router.register(r'testsuite2testcase', Testsuite2TestcaseViewSet)
router.register(r'testsuite_reports', TestsuiteReportsViewSet)

urlpatterns = [
    url(r'reports_details/', TestcaseReportsDetails.as_view()),
    url(r'testcases/batch/', TestcaseBatchAPIView.as_view()),
    url(r'testsuite/batch/', TestsuiteBatchAPIView.as_view()),
    path('login/', obtain_jwt_token),
    path('info/', get_user_info)
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

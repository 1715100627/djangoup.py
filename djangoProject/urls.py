"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls

# from projects.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projects.urls')),
    path('', include('envs.urls')),
    path('', include('interfaces.urls')),
    path('', include('debugtalks.urls')),
    path('', include('testsuits.urls')),
    path('', include('configures.urls')),
    path('', include('testcases.urls')),
    path('', include('testcase_reports.urls')),
    path('', include('summary.urls')),
    path('', include('module.urls')),
    path('docs/', include_docs_urls(title='接口文档',
                                    description='接口自动化测试平台')),
    path('api/', include('rest_framework.urls')),
    path('user/', include('user.urls'))
]

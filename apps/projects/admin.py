from django.contrib import admin
from projects.models import Projects


class ProjectsAdmin(admin.ModelAdmin):
    '定制后台管理类'

    # 指定修改(新增)中需要显示的字段
    fields = ('name', 'leader', 'tester', 'programmer', 'publish_app')
    # 指定列出字段
    list_display = ['id', 'name', 'leader', 'tester']


admin.site.register(Projects, ProjectsAdmin)

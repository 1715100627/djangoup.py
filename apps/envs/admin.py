from django.contrib import admin
from envs.models import Envs


class EnvsAdmin(admin.ModelAdmin):
    '定制后台管理类'

    # 指定修改(新增)中需要显示的字段
    fields = ('name', 'base_url', 'desc')
    # 指定列出字段
    list_display = ['name', 'base_url', 'desc']


admin.site.register(Envs, EnvsAdmin)

from django.db import models
from utils.base_models import BaseModel


class Envs(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='环境名称', max_length=200, unique=True, help_text='环境名称')
    base_url = models.URLField(verbose_name='请求base rul', max_length=200, help_text='请求base rul')
    desc = models.CharField(verbose_name='描述信息', max_length=200, help_text='描述信息')

    class Meta:
        db_table = 'db_envs'
        verbose_name = '环境信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

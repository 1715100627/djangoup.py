from django.db import models
from utils.base_models import BaseModel


class Projects(BaseModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="项目名称", max_length=200, unique=True, help_text='项目名称')
    leader = models.CharField(verbose_name='负责人', max_length=50, help_text='负责人', null=True, blank=True, default='',)
    envs = models.ManyToManyField(to='Envs', related_name='penvs', verbose_name='环境')
    # tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    # programmer = models.CharField(verbose_name='开发人员', max_length=50, help_text='开发人员', null=True, blank=True, default='',)
    # publish_app = models.CharField(verbose_name='发布应用', max_length=100, help_text='发布应用', null=True, blank=True,
    #                                default='', )
    desc = models.CharField(verbose_name='描述信息', max_length=200, null=True, blank=True, default='', help_text='描述信息')

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

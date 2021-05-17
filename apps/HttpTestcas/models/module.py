from django.db import models
from utils.base_models import BaseModel


class Module(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='模块名称', max_length=200, unique=True, help_text='模块名称')
    project = models.ForeignKey(to='Projects', related_name='models', on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name='所属项目')
    parent = models.ForeignKey(to='Module', related_name='+', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='父节点')
    floor = models.IntegerField(null=False, blank=False, default=1, verbose_name='树结构级数')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员',null=True, blank=True)
    desc = models.CharField(verbose_name='描述信息', max_length=200, help_text='描述信息', null=True, blank=True, default='', )

    class Meta:
        db_table = 'tb_models'
        verbose_name = '模块'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

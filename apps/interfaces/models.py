from django.db import models
from utils.base_models import BaseModel


class Interfaces(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='接口名称', max_length=200, unique=True, help_text='接口名称')
    # 第一个为关联的模型路径(应用名.模型类)
    # 第二个设置为父表删除，字表处理方式 CASCADE父表删除字表自动删除 SET_NULL被设置为none PROJECT报错 SET_DEFAULT设置默认值
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='interfaces', help_text='所属项目')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.TextField(verbose_name='简要描述', help_text='简要描述', blank=True, default='', null=True)

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

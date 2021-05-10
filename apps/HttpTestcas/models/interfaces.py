from django.db import models
from utils.base_models import BaseModel


class Interfaces(BaseModel):
    name = models.CharField(verbose_name='接口名称', max_length=200, unique=True, help_text='接口名称')
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    url = models.TextField(null=False, blank=False, verbose_name='接口请求URL')
    method_choice = (
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('POST', 'POST'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('OPTIONS', 'OPTIONS'),
        ('HEAD', 'HEAD'),
    )
    method = models.CharField(max_length=11, null=False, blank=False, default='GET', choices=method_choice,
                              verbose_name='接口请求方法')
    headers = models.TextField(null=True, blank=True, verbose_name='接口请求头信息')
    request_data_type_choice = (
        ('Json', 'Json'),
        ('Form Data', 'Form Data')
    )
    request_data_type = models.CharField(max_length=11, null=False, blank=False, default='Json',
                                         choices=request_data_type_choice, verbose_name='接口请求参数类型')
    request_data = models.TextField(null=True, blank=True, verbose_name='接口请求体参数')
    # 第一个为关联的模型路径(应用名.模型类)
    # 第二个设置为父表删除，字表处理方式 CASCADE父表删除字表自动删除 SET_NULL被设置为none PROJECT报错 SET_DEFAULT设置默认值
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='interfaces', help_text='所属项目')
    module = models.ForeignKey('module.Module', related_name='module', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='所属模块')
    envs = models.ForeignKey('envs.Envs', on_delete=models.CASCADE,
                                related_name='envs', help_text='运行环境')
    tester = models.CharField(verbose_name='测试人员', max_length=50, help_text='测试人员')
    desc = models.CharField(verbose_name='描述信息', max_length=200, null=True, blank=True, default='', help_text='描述信息')

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

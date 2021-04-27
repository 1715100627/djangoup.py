from django.db import models
from utils.base_models import BaseModel


class Testcases(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='用例名称', max_length=200, unique=True, help_text='用例名称')
    url = models.TextField(verbose_name='接口请求URL', null=True, blank=True)
    headers = models.TextField(verbose_name='接口请求头', null=True,blank=True)
    request_data_type_choice = (
        ('Json', 'Json'),
        ('Form Data', 'Form Data')
    )
    request_data_type = models.CharField(max_length=11, null=False, blank=False, default='Json',
                                         choices=request_data_type_choice, verbose_name='接口请求参数类型')
    request_params = models.TextField(verbose_name='接口查询参数', null=True, blank=True)
    request_data = models.TextField(verbose_name='接口请求参数', null=True, blank=True)
    expect_result = models.TextField(null=True, blank=True, verbose_name='期望结果')
    level_choice = (
        ('LOW', '低'),
        ('NORMAL', '中'),
        ('HIGH', '高'),
        ('HIGHER', '更高'),
    )
    level = models.CharField(max_length=12, null=False, blank=False, default='NORMAL', choices=level_choice,
                             verbose_name='用例级别')

    status_choice = (
        ('INITIAL', '初始状态'),
        ('PASS', '通过'),
        ('FAIL', '失败')
    )
    status = models.CharField(max_length=11, null=False, blank=False, default='INITIAL', choices=status_choice,
                              verbose_name='是否测试通过')
    api = models.ForeignKey(to='interfaces.Interfaces', related_name='testcase', on_delete=models.SET_NULL, null=True, blank=True,
                            verbose_name='所属接口')
    # testcase_folder = models.ForeignKey(to='TestcaseFolder', related_name='testcase_folder', on_delete=models.SET_NULL,
    #                                     null=True, blank=True, verbose_name='所属用例夹')

    class Meta:
        db_table = 'db_testcases'
        verbose_name = '测试用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

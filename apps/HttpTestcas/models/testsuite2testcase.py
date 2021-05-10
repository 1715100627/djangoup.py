from django.db import models
from utils.base_models import BaseModel


class Testsuite2Testcase(BaseModel):
    testsuite = models.ForeignKey(to='Testsuite', related_name='testsuite', on_delete=models.CASCADE,
                                  verbose_name='测试场景')
    testcases = models.ForeignKey(to='Testcases', related_name='testcases', on_delete=models.CASCADE,
                                  verbose_name='测试用例', null=True)
    type_choice = (
        ('HTTP_API', 'http api接口'),
        ('EXT_METHOD', '扩展方法')
    )
    type = models.CharField(max_length=16, null=False, blank=False, default='HTTP_API', choices=type_choice,
                            verbose_name='用例类型')
    ext_method_name = models.CharField(null=True, blank=True, max_length=128, verbose_name='扩展方法名称')
    ext_method = models.CharField(max_length=512, null=True, blank=True, verbose_name='扩展方法')
    sort = models.IntegerField(null=False, blank=False, verbose_name='排序')
    is_execute = models.BooleanField(null=False, blank=False, default=False, verbose_name='执行/跳过')
    loop_count = models.IntegerField(null=False, blank=False, default=1, verbose_name='循环次数')

    testsuite_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='测试场景名称')
    testcase_name = models.CharField(null=True, blank=True, max_length=128, verbose_name='测试场景名称')
    url = models.TextField(null=True, blank=True, verbose_name='接口请求URL')
    headers = models.TextField(null=True, blank=True, verbose_name='接口请求头')
    request_data_type_choice = (
        ('Json', 'Json'),
        ('Form Data', 'Form Data')
    )
    request_data_type = models.CharField(max_length=11, null=True, blank=True, choices=request_data_type_choice,
                                         verbose_name='接口请求参数类型')
    request_params = models.TextField(null=True, blank=True, verbose_name='接口查询参数')
    request_data = models.TextField(null=True, blank=True, verbose_name='接口请求参数')
    expect_result = models.TextField(null=True, blank=True, verbose_name='期望结果')

    class Meta:
        verbose_name = '场景用例'
        verbose_name_plural = verbose_name
        db_table = 'db_testsuite2testcase'

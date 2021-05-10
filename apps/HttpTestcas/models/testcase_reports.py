from django.db import models
from utils.base_models import BaseModel
from HttpTestcas.core.utils import get_version as version


class Reports(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    url = models.TextField(verbose_name='url', null=True, blank=True)
    method_choice = (
        ('GET', 'GET'),
        ('PUT', 'PUT'),
        ('POST', 'POST'),
        ('DELETE', 'DELETE')
    )
    method = models.CharField(max_length=11,null=False, blank=False, default='GET', choices=method_choice,
                              verbose_name='接口请求方法')
    headers = models.TextField(null=True, blank=True, verbose_name='接口请求头信息')
    request_data_type_choice = (
        ('Params', 'Params'),
        ('Json', 'Json'),
        ('Form Data', 'Form Data')
    )
    request_data_type = models.CharField(max_length=11, null=False, blank=False, default='Json',
                                         choices=request_data_type_choice, verbose_name='接口请求参数类型')
    request_data = models.TextField(null=True, blank=True, verbose_name='接口请求参数')
    actual_status_code = models.CharField(max_length=11, null=False, blank=False, verbose_name='实际响应状态码')
    actual_response_data = models.TextField(null=False, blank=False, verbose_name='实际响应结果')
    execute_time = models.DateTimeField(verbose_name='执行时间')
    elapsed_ms = models.DecimalField(max_digits=10, decimal_places=3, null=False, blank=False, verbose_name='响应时长(ms)')
    status_choice = (
        ('PASS', '通过'),
        ('FAIL', '失败')
    )
    status = models.CharField(max_length=11, null=False, blank=False, default='FAIL', choices=status_choice,
                              verbose_name='是否测试通过')
    failure_reason = models.TextField(null=True, blank=True, verbose_name='测试未通过原因')
    project = models.ForeignKey(to='projects.Projects', related_name='+', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='所属项目')
    project_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='项目名称')
    api = models.ForeignKey(to='interfaces.Interfaces', related_name='+', on_delete=models.SET_NULL, null=True, blank=True,
                            verbose_name='所属接口')
    api_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='接口名称')
    testcase = models.ForeignKey(to='testcases.Testcases', related_name='testcase_result', on_delete=models.SET_NULL, null=True,
                                 blank=True, verbose_name='所属用例')
    testcase_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='用例名称')

    is_periodictask = models.BooleanField(null=False, blank=False, default=True, verbose_name='是否是定时任务')
    version = models.CharField(max_length=13, null=False, blank=False, default=version, verbose_name='版本号')

    class Meta:
        db_table = 'db_testcase_reports'
        verbose_name = '用例测试报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.testcase_name

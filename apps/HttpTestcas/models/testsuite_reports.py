from utils.base_models import BaseModel
from django.db import models
from HttpTestcas.core.utils import get_version as version


class TestsuiteReports(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    execute_time = models.DateTimeField(verbose_name='执行时间')
    elapsed_ms = models.DecimalField(max_digits=10, decimal_places=3, null=False, blank=False, verbose_name='执行耗时(ms)')
    passed_num = models.IntegerField(null=False, blank=False, verbose_name='通过数量')
    failed_num = models.IntegerField(null=False, blank=False, verbose_name='失败数量')
    total_num = models.IntegerField(null=False, blank=False, verbose_name='用例总数量')
    status_choice = (
        ('PASS', '通过'),
        ('PARTIAL_PASS', '部份通过'),
        ('FAIL', '失败')
    )
    status = models.CharField(max_length=12, null=False, blank=False, default='FAIL', choices=status_choice,
                              verbose_name='是否测试通过')
    project = models.ForeignKey(to='Projects', related_name='+', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='所属项目')
    project_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='项目名称')
    testsuite = models.ForeignKey(to='Testsuite', related_name='testsuite_result', on_delete=models.SET_NULL, null=True,
                                  blank=True, verbose_name='所属场景')
    testsuite_name = models.CharField(null=False, blank=False, max_length=128, verbose_name='场景名称')
    # executor_real_name = models.CharField(null=False, blank=False, max_length=32, default='定时任务',
    #                                       verbose_name='执行人真空姓名')
    # is_periodictask = models.BooleanField(null=False, blank=False, default=True, verbose_name='是否是定时任务')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    version = models.CharField(max_length=13, null=False, blank=False, default=version, verbose_name='版本号')

    class Meta:
        db_table = 'db_testsuite_reports'
        verbose_name = '场景测试报告'
        verbose_name_plural = verbose_name

from django.db import models
from utils.base_models import BaseModel


class Testsuite(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='场景名称', max_length=200, unique=True, help_text='场景名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.SET_NULL, null=True,
                                blank=True,
                                related_name='project', help_text='所属项目 ')
    level_choice = (
        ('LOW', '低'),
        ('NORMAL', '中'),
        ('HIGH', '高'),
        ('HIGHER', '更高'),
    )
    level = models.CharField(max_length=12, null=False, blank=False, default='NORMAL', choices=level_choice,
                             verbose_name='场景级别')
    status_choice = (
        ('INITIAL', '初始状态'),
        ('FAIL', '全部失败'),
        ('PASS', '全部通过'),
        ('PARTIAL_PASS', '部分通过')
    )
    status = models.CharField(max_length=12, null=False, blank=False, default='INITIAL', choices=status_choice,
                              verbose_name='是否测试通过')
    testcases = models.ManyToManyField(to='testcases.Testcases', related_name='testsuite',
                                       # through='Testsuite2Testcase', through_fields=('testsuite', 'testcases'),
                                       verbose_name='测试用例')
    desc = models.CharField(verbose_name='描述信息', max_length=200, null=True, blank=True, default='', help_text='描述信息')

    class Meta:
        db_table = 'db_testsuits'
        verbose_name = '测试场景列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

from django.db import models
from utils.base_models import BaseModel


class Testsuits(BaseModel):
    id = models.AutoField(verbose_name='ID主键', primary_key=True, help_text='ID主键')
    name = models.CharField(verbose_name='套件名称', max_length=200, unique=True, help_text='套件名称')
    project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE,
                                related_name='testsuits', help_text='所属项目 ')
    include = models.TextField(verbose_name='包含接口', null=True, help_text='包含接口')

    class Meta:
        db_table = 'db_testsuits'
        verbose_name = '套件集'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

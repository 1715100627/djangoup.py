# Generated by Django 3.1.2 on 2021-03-31 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, help_text='逻辑删除', verbose_name='逻辑删除')),
                ('id', models.AutoField(help_text='ID主键', primary_key=True, serialize=False, verbose_name='ID主键')),
                ('name', models.CharField(help_text='模块名称', max_length=200, unique=True, verbose_name='模块名称')),
                ('floor', models.IntegerField(default=1, verbose_name='树结构级数')),
                ('tester', models.CharField(help_text='测试人员', max_length=50, verbose_name='测试人员')),
                ('desc', models.CharField(blank=True, default='', help_text='描述信息', max_length=200, null=True, verbose_name='描述信息')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='module.module', verbose_name='父节点')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='models', to='projects.projects', verbose_name='所属项目')),
            ],
            options={
                'verbose_name': '模块',
                'verbose_name_plural': '模块',
                'db_table': 'tb_models',
            },
        ),
    ]
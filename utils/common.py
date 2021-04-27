import json
import os
import yaml
from datetime import datetime
import logging
from django.conf import settings

from httprunner.task import HttpRunner
from httprunner.exceptions import ParamsError

from rest_framework import status
from rest_framework.response import Response

from testcases.models import Testcases
from envs.models import Envs
from testcase_reports.models import Reports
from debugtalks.models import Debugtalks
from configures.models import Configures


def timestamp_to_datetime(summary, type=True):
    # 格式化summary时间
    if not type:
        time_stamp = int(summary["time"]["start_at"])
        summary['time']['start_datetime'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

    for detail in summary['details']:
        try:
            time_stamp = int(detail['time']['start_at'])
            detail['time']['start_at'] = datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass

        for record in detail['records']:
            try:
                time_stamp = int(record['meta_data']['request']['start_timestamp'])
                record['meta_data']['request']['start_timestamp'] = \
                    datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                pass
    return summary


def generate_testcase_files(instance, env, testcase_path):
    # 生成yml文件
    testcase_list = []
    config = {'config': {
        'name': instance.name,
        'request': {
            'base_url': env.base_url if env else ''
        }
    }}
    testcase_list.append(config)

    # 获取当前用例配置和前置
    include = json.loads(instance.include)
    if include['testcases'] == None:
        include['testcases'] = []

    # 获取当前用例request
    request = json.loads(instance.request)
    request['test']['request']['verify'] = False

    # 获取接口名字
    interfaces_name = instance.interface.name
    project_name = instance.interface.project.name

    # 项目名路径
    testcase_path = os.path.join(testcase_path, project_name)

    # 创建项目名文件
    if not os.path.exists(testcase_path):
        os.makedirs(testcase_path)
        debugtalk_obj = Debugtalks.objects.filter(is_delete=False, project__name=project_name).first()

        if debugtalk_obj:
            debugtalk = debugtalk_obj.debugtalk
        else:
            debugtalk = ''
        with open(os.path.join(testcase_path, 'debugtalk.py'), mode='w', encoding='utf-8') as one_file:
            one_file.write(debugtalk)

    # 接口名路径
    testcase_path = os.path.join(testcase_path, interfaces_name)
    if not os.path.exists(testcase_path):
        os.mkdir(testcase_path)

    # 前置配置
    if 'config' in include:
        config_id = include.get('config')
        config_obj = Configures.objects.filter(is_delete=False, id=config_id).first()
        if config_obj:
            # setdefault如果键不存在于字典中，将会添加键并将值设为默认值。
            config_request = json.loads(config_obj.request)
            config_request['config']['request']['base_url'] = env.base_url
            testcase_list[0] = config_request

    # 前置用例
    if 'testcases' in include:
        for t_id in include.get('testcases'):
            testcase_obj = Testcases.objects.filter(is_delete=False, id=t_id).first()
            if testcase_obj:
                testcase_request = json.loads(testcase_obj.request)
                testcase_request['test']['request']['verify'] = False
                testcase_list.append(testcase_request)

    testcase_list.append(request)

    with open(os.path.join(testcase_path, instance.name + '.yml'),
              mode='w', encoding='utf-8') as one_file:
        yaml.dump(testcase_list, one_file, allow_unicode=True)


def create_report(runner, report_name=None):
    # 创建报告到数据库
    time_stamp = int(runner.summary["time"]["start_at"])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime(
        '%Y-%m-%d %H:%M:%S')
    runner.summary['time']['start_datetime'] = start_datetime
    # duration保留3位小数
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary['details']:
        try:
            for record in item['records']:
                record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            continue

    summary = json.dumps(runner.summary, ensure_ascii=False)

    report_name = report_name + '_' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    report_path = runner.gen_html_report(html_report_name=report_name)

    with open(report_path, encoding='utf-8') as stream:
        reports = stream.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary
        }

    report_obj = Reports.objects.create(**test_report)
    return report_obj.id


def run_testcase(instance, testcase_dir_path):
    # 运行
    runner = HttpRunner()
    runner.run(testcase_dir_path)
    runner.summary = timestamp_to_datetime(runner.summary, type=False)

    try:
        report_name = instance.name
    except Exception as e:
        report_name = '遗弃的报告' + '-' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')

    report_id = create_report(runner, report_name=report_name)
    data_dict = {
        'id': report_id
    }

    return Response(data_dict, status=status.HTTP_201_CREATED)

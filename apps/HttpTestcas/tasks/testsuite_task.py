from celery import shared_task
from HttpTestcas.models import Testsuite
from HttpTestcas.core.utils import get_version
import threading
from HttpTestcas.core.http_dlient import HttpSession
from HttpTestcas.core.http_testsuite_run import HttpTestsuiteRun
from apps.HttpTestcas.models.testcase_reports import TestcaseReports
from apps.HttpTestcas.models.testcases import Testcases


def run_testsuite(testsuite=None, version=None):
    for testsuite in testsuite:
        project = testsuite.project
        # 获取场景集所属项目环境
        envs = project.default_envs
        # 4创建HttpSession实例
        http_session = HttpSession()
        # 5创建HttpTestcaseRunner实例
        http_testsuite_run = HttpTestsuiteRun(project=project, envs=envs, testsuite=testsuite,
                                              http_session=http_session)

        testsuite_result, testcase_result_list = http_testsuite_run.run()
        testsuite_result.version = version

        testcase_list = []
        for testcase_result in testcase_result_list:
            testcase_result.testsuite_result = testsuite_result
            testcase_result.version = version
            testcase = testcase_result.testcase
            testcase.status = testcase_result.status
            testcase_list.append(testcase)

        # 1、保存场景结果
        testsuite_result.save()
        # 2、更新场景状态
        testsuite.status = testsuite_result.status
        testsuite.save()
        # 更新测试用例报告及用例状态
        TestcaseReports.objects.bulk_create(testcase_result_list)
        Testcases.objects.bulk_update(testcase_list, fields=['status'])


@shared_task
def batch_exec_testsuite(testsuites=None, version=None):
    pass
    if not version:
        version = get_version()

    if isinstance(testsuites, str):
        testsuites = eval(testsuites) if isinstance(eval(testsuites), list) else []
    testsuite_list = Testsuite.objects.filter(id__in=testsuites, is_delete=False)

    # 线程数量
    thread_num = 5
    # Q每个线程多少任务   R剩余
    Q, R = divmod(len(testsuite_list), thread_num)

    # 生成线程对应数量的列表
    testcases_temp = [[] for i in range(thread_num)]

    # 每次取出Q个用例放入testcases_temp里的list中
    for i in range(thread_num):
        testcases_temp[i] = testsuite_list[i * Q:(i + 1) * Q]

    for i in range(R):
        testcases_temp[i].append(testsuite_list[Q * R + i])

    # 给线程分配任务并启动
    threads = []
    for y in range(thread_num):
        t = threading.Thread(target=run_testsuite, args=(testcases_temp[y], version))
        threads.append(t)

    for t in threads:
        t.start()

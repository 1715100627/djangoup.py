from celery import shared_task

from HttpTestcas.core.http_dlient import HttpSession
from HttpTestcas.core.http_testcase_run import HttpTestcaseRun
from HttpTestcas.models import Testcases
import threading
from HttpTestcas.core.utils import get_version
from HttpTestcas.models import TestcaseReports


def run_testcase(testcases=None, version=None):
    # 报告结果列表,版本号
    testcase_version_list = []
    # 用例执行后状态结果列表
    testcase_status = []
    for testcase in testcases:
        # 1获取接口信息
        api = testcase.api
        # 2获取接口运行环境
        env = api.envs
        # 3获取接口所属项目
        project = api.project
        # 4创建HttpSession实例
        http_session = HttpSession()
        # 5创建HttpTestcaseRunner实例
        http_testcase_run = HttpTestcaseRun(http_session=http_session, env=env, project=project, testcases=testcase,
                                            api=api)
        testcase_result_list = http_testcase_run.run()
        for testcase_list in testcase_result_list:
            testcase_list.version = version
            testcase_version_list.append(testcase_list)
            if testcase_list:
                testcase.status = testcase_list.status
                testcase_status.append(testcase)
    TestcaseReports.objects.bulk_create(testcase_version_list)
    Testcases.objects.bulk_update(testcase_status, fields=['status'])


@shared_task
def batch_exec_testcase(testcases=None, version=None):
    if not version:
        # 执行定时任务时，参数version为None，此需要设置version；当批量执行时，参数version为传入值
        version = get_version()

    if isinstance(testcases, str):
        testcases = eval(testcases) if isinstance(eval(testcases), list) else []
    testcases_list = Testcases.objects.filter(id__in=testcases, is_delete=False)

    # 线程数量
    thread_num = 5
    # Q每个线程多少任务   R剩余
    Q, R = divmod(len(testcases_list), thread_num)

    # 生成线程对应数量的列表
    testcases_temp = [[] for i in range(thread_num)]

    # 每次取出Q个用例放入testcases_temp里的list中
    for i in range(thread_num):
        testcases_temp[i] = testcases_list[i * Q:(i + 1) * Q]

    for i in range(R):
        testcases_temp[i].append(testcases_list[Q * R + i])

    # 给线程分配任务并启动
    threads = []
    for y in range(thread_num):
        t = threading.Thread(target=run_testcase, args=(testcases_temp[y], version))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

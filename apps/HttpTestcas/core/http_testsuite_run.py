from django.utils import timezone
from HttpTestcas.core.http_testcase_run import *
from apps.HttpTestcas.models import TestsuiteReports


class HttpTestsuiteRun(object):
    def __init__(self, project=None, envs=None, testsuite=None, http_session=None):
        self.http_session = http_session
        self.project = project
        self.envs = envs
        self.testsuite = testsuite

    def run(self):
        testsuite_testcase_list = self.testsuite.testsuite2testcase.all()
        testsuite_result_mapping = {
            "execute_time": timezone.now(),
            "elapsed_ms": 0,
            "passed_num": 0,
            "failed_num": 0,
            "total_num": 0,
            "status": "PASS",
            "project_id": self.testsuite.project.id,
            "project_name": self.testsuite.project.name,
            "testsuite_id": self.testsuite.id,
            "testsuite_name": self.testsuite.name,
        }
        testcase_result_list = []
        for testsuite_testcase in testsuite_testcase_list:
            # 判断是否执行
            is_run = testsuite_testcase.is_execute
            if is_run:
                if testsuite_testcase.type == 'HTTP_API':
                    # 组织用例信息
                    testcase = testsuite_testcase.testcase
                    api = testcase.api
                    envs = api.envs
                    if not envs:
                        envs = self.envs

                    # 初始化testcase
                    http_testcase_runner = HttpTestcaseRun(http_session=self.http_session, env=envs,
                                                           project=self.project, api=api, testcases=testcase)
                    temp_testcase_result_list = http_testcase_runner.run()
                    testsuite_result_mapping["total_num"] += len(temp_testcase_result_list)
                    for temp_testcase_result in temp_testcase_result_list:
                        temp_testcase_result.testsuite_name = self.testsuite.name
                        testcase_result_list.append(temp_testcase_result)
                        testsuite_result_mapping["elapsed_ms"] += (
                            temp_testcase_result.elapsed_ms if temp_testcase_result else 0)
                        if temp_testcase_result is None or temp_testcase_result.status == 'FAIL':
                            testsuite_result_mapping['failed_num'] += 1
                            testsuite_result_mapping["status"] = "FAIL"
                        elif temp_testcase_result and temp_testcase_result.status == "PASS":
                            testsuite_result_mapping["passed_num"] += 1

                        if testsuite_result_mapping['passed_num'] == testsuite_result_mapping["total_num"]:
                            testsuite_result_mapping["status"] = "PASS"
                        elif testsuite_result_mapping["failed_num"] > 0 and testsuite_result_mapping["passed_num"] > 0:
                            testsuite_result_mapping["status"] = "PARTIAL_PASS"
                        elif testsuite_result_mapping["failed_num"] == testsuite_result_mapping["total_num"]:
                            testsuite_result_mapping["status"] = "FAIL"
                    testsuite_result = TestsuiteReports(**testsuite_result_mapping)
                    # 更近数据与报告
                    return testsuite_result, testcase_result_list

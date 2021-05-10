import json
from .validators import Validator
from testcase_reports.models import Reports


class HttpTestcaseRun(object):
    def __init__(self, http_session=None, env=None, project=None, api=None, testcases=None):
        self.http_session = http_session
        self.env = env
        self.project = project
        self.api = api
        self.testcases = testcases

    def run(self, testcase_name=None, url=None, headers=None, request_params=None, request_data_type=None,
            request_data=None, expect_result=None, executor=None, ):
        # 组织用例信息
        testcase_name = self.testcases.name
        testcase_url = self.testcases.url
        headers = json.loads(self.testcases.headers)
        request_params = self.testcases.request_params
        request_data_type = self.testcases.request_data_type
        request_data = json.loads(self.testcases.request_data)
        expect_result = json.loads(self.testcases.expect_result)
        method = self.api.method.upper()

        # 组织请求头
        request_kwargs = dict(
            headers=headers
        )
        if request_data_type == "Json":
            request_kwargs.update({"json": request_data})
        elif request_data_type == "Form Data":
            request_kwargs.update({"data": request_data})

        if testcase_url.startswith('http') or testcase_url.startswith('https'):
            pass
        else:
            testcase_url = self.env.url + testcase_url

        res_obj = self.http_session.request(url=testcase_url, method=method, **request_kwargs)

        res_key = res_obj['response'].keys()
        actual_key = list(set(res_key).intersection(['results', 'text', 'content']))[0]
        res_value = ''
        if isinstance(res_obj['response'][actual_key], str):
            res_value = res_obj['response'][actual_key]
        else:
            res_value = json.dumps(res_obj["response"][actual_key], ensure_ascii=False)

        # 断言 创建校验器
        validator = Validator()

        # 格式化validate
        validator.uniform_validate(expect_result.get('validate'))

        # 校验预期结果与实际结果
        results, calibration = validator.validate(res_obj=res_obj['response'])
        testcase_result_list = []
        testcase_result = {
            "project_id": self.project.id,
            "project_name": self.project.name,
            "api_id": self.api.id,
            "api_name": self.api.name,
            "testcase_id": self.testcases.id,
            "testcase_name": testcase_name,
            "method": method,
            "url": testcase_url,
            "request_data_type": request_data_type,
            "headers": json.dumps(headers, ensure_ascii=False),
            "request_data": json.dumps(request_data, ensure_ascii=False),
            "actual_status_code": res_obj["response"]["status_code"],
            "actual_response_data": res_value,
            "execute_time": res_obj["stat"]["execute_time"],
            "elapsed_ms": res_obj["response"]["elapsed"],
            "status": results
        }
        if results == 'FAIl':
            testcase_result.update({
                'failure_reason': json.dumps(calibration, ensure_ascii=False)
            })

        testcase_result = Reports(**testcase_result)
        testcase_result_list.append(testcase_result)
        return testcase_result_list

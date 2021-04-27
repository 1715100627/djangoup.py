import json
from .validators import Validator


class HttpTestcaseDebug(object):
    def __init__(self, http_session=None, name=None, url=None, method=None, cookies=None,
                 headers=None, request_data_type=None, json_data=None, form_data=None, expect_result=None):
        self.http_session = http_session
        self.name = name
        self.url = url
        self.method = method
        self.headers = headers
        self.request_data_type = request_data_type
        self.json_data = json_data
        self.form_data = form_data
        self.expect_result = expect_result

    def debug(self):
        request_kwargs = dict(
            headers=self.headers,
            data=self.form_data,
            json=self.json_data
        )
        res_obj = self.http_session.request(url=self.url, method=self.method, **request_kwargs)
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
        validator.uniform_validate(self.expect_result.get('validate'))

        # 校验预期结果与实际结果
        results, calibration = validator.validate(res_obj=res_obj['response'])

        testcase_result = {
            "url": self.url,
            "method": self.method,
            "headers": json.dumps(self.headers, ensure_ascii=False),
            "request_data": json.dumps(self.json_data or self.form_data, ensure_ascii=False),
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
        return testcase_result

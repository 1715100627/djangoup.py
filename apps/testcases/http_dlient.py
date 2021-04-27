import requests
from django.utils import timezone


class HttpSession(requests.Session):
    def __init(self):
        self._response_meta()

    def _response_meta(self):
        self.response_data = {
            'response': {
                'url': '',
                'headers': {},
                'status_code': 200,
                'elapsed': 0,
                "results": None,
                "content": None,
                "text": None,
            },
            "stat": {
                "execute_time": None,
            }
        }

    def request(self, url, method, **kwargs):
        self._response_meta()

        # 记录当前时间
        execute_time = timezone.now()
        self.response_data['stat'].update({"execute_time": execute_time})

        response = requests.Session.request(self, method=method, url=url, **kwargs)
        self.response_data['response'] = self._response_seal(response)

        return self.response_data

    @staticmethod
    def _response_seal(res_obj):
        response_dict = dict()
        response_dict['url'] = res_obj.url
        response_dict['status_code'] = res_obj.status_code
        response_dict['headers'] = dict(res_obj.headers)
        response_dict['elapsed'] = res_obj.elapsed.microseconds / 1000.0

        content_type = dict(res_obj.headers).get('Content-Type')
        if "application/json" in content_type:
            response_dict["content"] = res_obj.content
        elif "text/html" in content_type:
            response_dict["text"] = res_obj.text

        return response_dict

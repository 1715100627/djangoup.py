import re

json = {"count": 3,
        "next": "http://127.0.0.1:8000/projects/?p=2",
        "previous": 'null',
        "results": [{"id": 1, "create_time": "2020-11-02T10:52:47.906621Z",
                     "name": "321项目",
                     "leader": "321",
                     "tester": "321",
                     "programmer": "3212",
                     "publish_app": "", "desc": ""},
                    {"id": 2,
                     "create_time": "2020-11-02T10:54:11.741749Z",
                     "name": "123项目",
                     "leader": "123",
                     "tester": "123",
                     "programmer": "123",
                     "publish_app": "",
                     "desc": ""}]}

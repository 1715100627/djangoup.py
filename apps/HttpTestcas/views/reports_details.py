from rest_framework.response import Response

from testcase_reports.models import Reports
from rest_framework.views import APIView
from django.db.models import Sum
from testcase_reports.serializer import ReportsSerializer


class TestcaseReportsDetails(APIView):
    # 报告列表数据
    def get(self, request, *args, **kwargs):
        # 版本号
        version = request.query_params.get('version')
        status = request.query_params.get('status', None)
        if version:
            testcase_results = Reports.objects.filter(version=version, is_delete=False)
            testcase_count = testcase_results.count()
            success = testcase_results.filter(status='PASS').count()
            fail = testcase_results.filter(status='FAIL').count()
            run_time = testcase_results.aggregate(Sum('elapsed_ms'))['elapsed_ms__sum']

            success_rate = round(((success / testcase_count) * 100), 2)

            if status:
                testcase_results = testcase_results.filter(status='status')

            data = []
            for i in testcase_results:
                testcase_result = ReportsSerializer(i).data
                data.append(testcase_result)
            response = {
                'testcase_count': testcase_count,
                'success': success,
                'fail': fail,
                'success_rate': success_rate,
                'run_time': run_time,
                'results': data
            }

            return Response({
                "code": 200,
                "data": {'data': response},
                "message": "OK",
            })

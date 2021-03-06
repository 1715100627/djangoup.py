import re
from HttpTestcas.models import Interfaces
from django.db.models import Count
# from testsuite.models import Testsuite

def get_paginated_response(datas):
    list = []
    for item in datas:
        mtch1 = item['create_time'].split('T')[0]
        # mtch2 = item['create_time'].split('T')[1].split('+')[0] +' '+ item['create_time'].split('T')[1].split('+')[1]
        mtch2 = item['create_time'].split('T')[1].split('.')[0]
        item['create_time'] = mtch1 + ' ' + mtch2

        # project_id = item['id']
        # # Interfaces.objects.filter(project_id=project_id,is_delete=False)
        # interfaces_testcases_objs = Interfaces.objects.values('id').annotate(testcases=Count('testcases')). \
        #     filter(project_id=project_id, is_delete=False)
        #
        # # 接口总数
        # interfaces_count = interfaces_testcases_objs.count()
        #
        # testcases_count = 0
        # for one_dict in interfaces_testcases_objs:
        #     testcases_count += one_dict['testcases']
        #
        #
        # #配置总数
        # interfaces_configures_objs = Interfaces.objects.values('id').annotate(configures=Count('configures')). \
        #     filter(project_id=project_id, is_delete=False)
        # configures_count = 0
        # for one_dict in interfaces_configures_objs:
        #     configures_count += one_dict['configures']
        #
        #
        # # 套件总数
        # testsuits_count = Testsuits.objects.filter(project_id=project_id,is_delete=False).count()

        # item['interfaces'] = interfaces_count
        # item['testsuite'] = testsuits_count
        # item['testcases'] = testcases_count
        # item['configures'] = configures_count

        list.append(item)
    return list


def get_paginated_response_update(datas):
    list = []
    for i in datas:
        # mtch = re.search(r'(.*)T(.*)\..*?', i['update_time'])
        # i['update_time'] = mtch.group(1) + ' ' + mtch.group(2)
        mtch1 = i['update_time'].split('T')[0]
        mtch2 = i['update_time'].split('T')[1].split('.')[0]
        i['update_time'] = mtch1 + ' ' + mtch2
        list.append(datas)
    return list

def get_paginated_response_create(datas):
    # list = []
    for i in datas:
        # mtch = re.search(r'(.*)T(.*)\..*?', i['create_time'])
        # i['create_time'] = mtch.group(1) + ' ' + mtch.group(2)
        mtch1 = i['create_time'].split('T')[0]
        mtch2 = i['create_time'].split('T')[1].split('.')[0]
        i['create_time'] = mtch1 + ' ' + mtch2
    return datas

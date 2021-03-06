def handle_param_type(value):
    if isinstance(value, int):
        param_type = 'int'
    elif isinstance(value, float):
        param_type = 'float'
    elif isinstance(value, bool):
        param_type = 'bool'
    else:
        param_type = 'string'
    return param_type


def handle_data1(datas):
    # 将后端json格式转换为前端嵌套字典列表
    result_list = []
    if datas:
        for key, value in datas.items():
            result_list.append({
                'key': key,
                'value': value
            })
    return result_list


def handle_data2(datas):
    # 嵌套字典列表转换[{key:'age',param_type:'int'}]
    result_list = []
    if datas:
        for one_var_list in datas:
            key = list(one_var_list)[0]
            value = one_var_list.get(key)
            result_list.append({
                'key': key,
                'value': value,
                'param_type': handle_param_type(value)
            })
    return result_list


def handle_data3(datas):
    # 断言处理
    result_list = []
    if datas:
        for one_var_list in datas:
            key = one_var_list.get('check')
            value = one_var_list.get('expected')
            comparator = one_var_list.get('comparator')

            result_list.append({
                'key': key,
                'value': value,
                'comparator': comparator,
                'param_type': handle_param_type(value)
            })
    return result_list


def handle_data4(datas):
    # 将{'user':'123','gender':True}转换为[{key:'user',value:'123',param_type:'string'}]
    result_list = []
    if datas:
        for key, value in datas.items():
            result_list.append({
                'key': key,
                'value': value,
                'param_type': handle_param_type(value)
            })
    return result_list


def handle_data5(datas):
    # 将[{'token':'content.token'}]转换为 ['key':'token',value:'content.token']
    result_list = []
    if datas:
        for one_dict in datas:
            key = list(one_dict)[0]
            value = one_dict.get(key)
            result_list.append({
                'key': key,
                'value': value
            })
    return result_list


def handle_data6(datas):
    result_list = []
    if datas:
        for item in datas:
            result_list.append({
                'key': item
            })
    return result_list

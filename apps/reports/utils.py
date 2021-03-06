import re


def format_output(datas):
    datas_list = []
    for i in datas:
        result = 'pass' if i['result'] else 'Fail'
        form_time = i['create_time'].split('T')
        first_part = form_time[0]
        second_part = form_time[1].split('.')[0]
        f_time = first_part + ' ' + second_part
        i['create_time'] = f_time
        i['result'] = result
        datas_list.append(i)
    return datas_list


def get_file_contents(filename, chunk_size=512):
    with open(filename, encoding='utf-8') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

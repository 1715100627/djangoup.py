import time


def get_version():
    '''
    获取毫秒时间戳字符串，长度为13位
    :return:
    '''
    return str(int(time.time() * 1000))
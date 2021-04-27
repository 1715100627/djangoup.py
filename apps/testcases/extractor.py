import jsonpath


class Extractor(object):
    def __init__(self):
        pass

    @staticmethod
    def extract_jsonpath(res_obj=None, expr=None):
        result = jsonpath.jsonpath(res_obj, expr)
        if result == False:
            print('未提取到值')
        elif isinstance(result,list):
            if len(result) == 1:
                result = result[0]
        return result
from .loader import load_validators
from .extractor import Extractor


class Validator(object):
    def __init__(self):
        self.validate_list = []

    def uniform_validate(self, validate_variables):
        if isinstance(validate_variables, list):
            for item in validate_variables:
                self.uniform_validate(item)
        elif isinstance(validate_variables, dict):
            if 'check' in validate_variables.keys() and 'expect' in validate_variables.keys():
                check_item = validate_variables.get('check')
                expect_value = validate_variables.get('expect')
                comparator = validate_variables.get('comparator')
                self.validate_list.append({
                    'check': check_item,
                    "expect": expect_value,
                    "comparator": comparator
                })
            else:
                print('校验参数错误')

    def validate(self, res_obj=None):
        validate_pass = 'PASS'

        # 加载所有校验器
        comparators_built = load_validators()
        # 记录
        failure_reason = []
        for validate_variable in self.validate_list:
            try:
                check_item = validate_variable['check']
                expect_value = validate_variable['expect']
                comparators = validate_variable['comparator']
                # 提取轻轻返回值实际结果
                actual_value = Extractor.extract_jsonpath(res_obj=res_obj, expr=check_item)
                failure_reason.append({
                    '检查项': check_item,
                    '期望值': expect_value,
                    '实际值': actual_value,
                    '断言方法': comparators,
                })

                # 校验
                fun = comparators_built[comparators]
                fun(actual_value=actual_value, expect_value=expect_value)
            except (AssertionError, TypeError):
                validate_pass = 'FAIL'
                continue
            else:
                failure_reason = []
        return validate_pass, failure_reason
from nose_parameterized import parameterized

def even_case_name(testcase_func, param_num, param):
  (value,) =  param.args
  return parameterized.to_safe_name(str(testcase_func.__name__ + "_custom_" + str(value)))

def get_values():
    return [ (0,), (1,), (2,), (3,), (4,), (5,) ]

@parameterized.expand(get_values(),
                      testcase_func_name=even_case_name)
def test_even(i):
    assert i % 2 == 0

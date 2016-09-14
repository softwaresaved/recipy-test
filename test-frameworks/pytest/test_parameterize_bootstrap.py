import os
import pytest

@pytest.fixture(scope="module")
def some_context():
    return [1,2,3,4,5]

def get_scripts():
    with open(config_file) as f:
        scripts = [line.strip('\n') for line in f.readlines()]
    return scripts

config_file = os.environ["RECIPY_TEST_CASES_CONFIG"]

def case_name(value):
    return "script_" + str(value)

@pytest.mark.parametrize("script", get_scripts(), ids=case_name)
def test_script(some_context, script):
    print(some_context)
    if script == "sklearn":
        pytest.fail(script, " failed its test")
    else:
        pass

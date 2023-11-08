import configparser
import pytest
from CommonLib.Logger import *


def pytest_configure():
    conf = configparser.ConfigParser()
    conf.read('..\..\pytest.ini')
    log_path = conf.get('log', 'log_file')
    # log_file_format = conf.get('log', 'log_file_format')
    log_file_level = conf.get('log', 'log_file_level')
    testcase_name = os.path.basename(os.getcwd())
    start_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
    log_path += "%s_%s.log" % (testcase_name, start_time)
    return_info = {'log_path': log_path, 'log_file_level': log_file_level}
    return return_info


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if item.iter_markers(name='must_pass'):
        if call.excinfo is not None:
            parent = item.parent
            parent._mpfailed = item

    # 记录测试结果到日志
    result = outcome.get_result()
    log_file = logger.log_path
    try:
        with open(log_file, "a") as f:
            f.write(result.nodeid + "   " + str(result.when) + "    " + str(result.outcome) + "    " + str(
                result.duration) + '\n')
    except Exception as e:
        print("Error", e)

    # 如果测试没pass直接结束
    must_pass_failed = getattr(item.parent, '_mpfailed', None)
    if must_pass_failed is not None:
        pytest.skip('must pass test failed (%s %s)' % (must_pass_failed.name, result.when))

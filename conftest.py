import configparser
import time


# def pytest_addoption(parser):
#     parser.addoption(
#         "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
#     )
#     # 添加参数到pytest.ini
#     parser.addini('url', type=None, default="http://49.235.92.12:8200/", help='添加 url 访问地址参数')

def pytest_configure():
    conf = configparser.ConfigParser()
    conf.read('D:\PythonProjects\AutoTest_yijianren\pytest.ini')
    log_path = conf.get('log', 'log_file')
    # log_file_format = conf.get('log', 'log_file_format')
    log_file_level = conf.get('log', 'log_file_level')
    log_path += "%s_%s.log" % (file_case, time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time())))
    return {'log_path': log_path, 'log_file_level': log_file_level}

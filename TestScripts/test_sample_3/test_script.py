from test_config import *
from CommonLib.BaseTest import *
from CommonLib.cmd_ethtool import *


# 继承StandardBaseTest类的基础testcase写法1
# setup与teardown前后只执行一次

class Test_AutoTest(StandardBaseTest):

    def test_handle_1(self):
        self.logger.info('1.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        assert retcode == 0

        self.logger.info('2.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        assert retcode == -1

    def test_handle_2(self):
        self.logger.info('1.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        assert retcode == 0

        self.logger.info('2.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        assert retcode == -1

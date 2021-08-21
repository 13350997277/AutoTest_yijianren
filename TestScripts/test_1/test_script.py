from test_config import *
from CommonLib.BaseTest import *
from CommonLib.cmd_ethtool import *


class Test_AutoTest(BaseTest):

    def test_handle(self):
        print('1.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(),**test_parameters)
        assert retcode == -1

        print('2.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(),**test_parameters)
        assert retcode == -1

    def test_recover(self):
        print('3.环境恢复')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters)
        assert retcode == -1
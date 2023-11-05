from test_config import *
from CommonLib.BaseTest import *
from CommonLib.cmd_ethtool import *


# 不继承StandardBaseTest类的基础testcase写法2
# setup与teardown前后只执行一次

class Test_AutoTest():
    def setup_class(self):
        print("==========初始化环境==========")
        self.env = Env_Clinet
        client = Terminal(Env_Clinet.get('ip'), Env_Clinet.get('port'), Env_Clinet.get('username'),
                          Env_Clinet.get('password'))
        client.connect()
        self.client = client

    def test_handle_1(self):
        print('1.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        assert retcode == 0

        print('2.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        assert retcode == -1

    def test_handle_2(self):
        print('1.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        assert retcode == 0

        print('2.查询设备信息')
        retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        assert retcode == -1

    def teardown_class(self):
        print("==========断开环境连接==========")
        self.client.close()

from test_config import *
from CommonLib.BaseTest import *
from CommonLib.cmd_ethtool import *


# 不继承StandardBaseTest类的基础testcase写法2
# setup与teardown前后只执行一次

class Test_AutoTest():
    # @pytest.mark.must_pass
    def setup_class(self):
        self.logger = logger.logger
        self.logger.info("==========初始化环境==========")
        self.tmu_com = Env_Pair.get('TMU_COM')
        client = Terminal(self.tmu_com.get('ip'), self.tmu_com.get('username'),
                          self.tmu_com.get('password'), self.tmu_com.get('port'), self.tmu_com.get('speed'))
        client.connect()
        self.client = client

    def test_handle_1(self):
        self.client.send_cmd('application-dft version tmu')
        # self.logger.info('1.查询设备信息')
        # retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        # assert retcode == 0
        #
        # self.logger.info('2.查询设备信息')
        # retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        # assert retcode == -1

    def test_handle_2(self):
        pass
        # self.logger.info('1.查询设备信息')
        # retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[0])
        # assert retcode == 0
        #
        # self.logger.info('2.查询设备信息')
        # retcode, retstr = self.client.exec_cmd(ethtool(), **test_parameters[1])
        # assert retcode == -1

    def teardown_class(self):
        self.logger.info("==========断开环境连接==========")
        self.client.close()


if __name__ == '__main__':
    pytest.main(['test_script.py', '-s'])

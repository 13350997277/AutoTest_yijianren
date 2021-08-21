from test_config import *
from TestConfig.BaseTest import *


class Test_AutoTest(BaseTest):

    def test_handle(self):
        stdin, stdout, stderr = self.client.exec_command('df -h')
        print(stdout.read().decode('utf-8'))
        print('test_handle called.')
        assert 1 == 2

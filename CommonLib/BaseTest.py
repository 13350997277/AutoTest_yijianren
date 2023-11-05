import pytest

from CommonLib.Terminal import *
from TestConfig.Environment import *
from CommonLib.Logger import *


@pytest.fixture(scope='class')
def setup_and_teardown(request):
    request.cls.logger = MyLogger().logger
    request.cls.logger.info("==========初始化环境==========")
    request.cls.env = Env_Clinet
    client = Terminal(Env_Clinet.get('ip'), Env_Clinet.get('port'), Env_Clinet.get('username'),
                      Env_Clinet.get('password'))
    client.connect()
    request.cls.client = client
    yield
    request.cls.logger.info("==========断开环境连接==========")
    request.cls.client.close()


@pytest.mark.usefixtures('setup_and_teardown')
class StandardBaseTest:
    pass

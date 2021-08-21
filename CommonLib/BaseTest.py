import pytest

from CommonLib import Client


@pytest.fixture(scope='class')
def client_init(request):
    print("初始化环境")
    client = Client.Client('192.168.22.128', 22, 'root', 'Huawei12#$')
    client.connect()
    request.cls.client = client
    yield
    print("断开环境连接")
    client.close()


@pytest.mark.usefixtures('client_init')
class BaseTest:
    pass

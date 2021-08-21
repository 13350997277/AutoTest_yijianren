import pytest
import paramiko

@pytest.fixture(scope='class')
def ssh_client_init(request):
    print("ssh_client_init called.")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname='192.168.22.128', port=22, username='root', password='Huawei12#$')
    request.cls.client = client
    yield
    print("ssh_client_close called.")
    client.close()

@pytest.mark.usefixtures('ssh_client_init')
class BaseTest():
    pass
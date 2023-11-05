import paramiko
import serial
from CommonLib.BaseCmd import *
from CommonLib.Logger import *


class Terminal():
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.type = ''
        self.logger = MyLogger().logger
        # ssh连接
        if self.port == 22:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.type = 'SSH'
        # com连接
        elif 'COM' in self.port:
            self.client = serial.Serial(port, host, 3)
            self.type = 'COM'
        # telnet连接
        else:
            pass

    def connect(self):
        if self.type == 'SSH':
            self.client.connect(hostname=self.host, port=self.port, username=self.username,
                                password=self.password)
            self.logger.info('连接成功：host=%s port=%s' % (self.host, self.port))
        # elif self.type == 'COM':

    def close(self):
        self.client.close()
        self.logger.info('连接关闭成功：host=%s port=%s' % (self.host, self.port))

    def send_cmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin, stdout, stderr = stdin, stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
        self.logger.info('命令发送成功:\n cmd=%s\n stdout=%s\n stderr=%s\n' % (
            cmd, stdout, stderr))
        return stdout, stderr

    def exec_cmd(self, cmd_cls: Base_Cmd, **option_args):
        retcode, retstr = -1, ''
        if not hasattr(self, 'cmd_%s' % str(cmd_cls.cmd_head)):
            self.check_cmd(cmd_cls)
            return self.exec_cmd(cmd_cls, **option_args)
        elif getattr(self, 'cmd_%s' % str(cmd_cls.cmd_head)) is True:
            self.logger.info('命令:%s 可用' % cmd_cls.cmd_head)
            retcode, cmd = cmd_cls.cmd_makeup(**option_args)
            if retcode != 0:
                return retcode, retstr
            stdout, stderr = self.send_cmd(cmd)
            retcode, retstr = cmd_cls.handle_ret(stdout, stderr, **option_args)
            return retcode, retstr
        else:
            self.logger.warning('不支持命令:%s' % cmd_cls.cmd_head)
            return retcode, retstr

    def check_cmd(self, cmd_cls: Base_Cmd):
        stdout, stderr = self.send_cmd(cmd_cls.cmd_head)
        if cmd_cls.cmd_check_available(stdout, stderr):
            setattr(self, 'cmd_%s' % str(cmd_cls.cmd_head), True)
        else:
            setattr(self, 'cmd_%s' % str(cmd_cls.cmd_head), False)

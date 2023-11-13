import paramiko
import serial
from CommonLib.BaseCmd import *
from CommonLib.Logger import *


class Terminal():
    def __init__(self, ip, username, password, port=None, speed=115200):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.speed = speed
        self.type = ''
        self.logger = logger.logger
        # ssh连接
        if self.port == 22:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.type = 'SSH'
        # com连接
        elif 'COM' in self.port:
            self.client = serial.Serial(port, speed, timeout=3)
            self.type = 'COM'
        # telnet连接
        else:
            pass

    def connect(self):
        if self.type == 'SSH':
            self.client.connect(hostname=self.ip, port=self.port, username=self.username,
                                password=self.password)
            self.logger.info('ssh连接成功：host=%s port=%s' % (self.ip, self.port))
        elif self.type == 'COM':
            if self.client.isOpen():
                self.client.write('\r'.encode('utf-8'))
                read = self.client.readlines()
                for line in read:
                    self.logger.info(line)
                if 'login:' in read[-1].decode(encoding='utf-8'):
                    self.client.write(self.username.encode('utf-8'))
                    self.client.write('\r'.encode('utf-8'))
                    read = self.client.read_until('Password:', 10240)
                    self.logger.info(read)
                    self.client.write(self.password.encode('utf-8'))
                    self.client.write('\r'.encode('utf-8'))
                    self.logger.info('com连接成功：host=%s port=%s' % (self.ip, self.port))
                elif 'hkzy-ast2600:~#' in read[-1].decode(encoding='utf-8'):
                    self.logger.info('com连接成功：host=%s port=%s' % (self.ip, self.port))
            else:
                self.logger.error('com连接失败：host=%s port=%s' % (self.ip, self.port))

    def close(self):
        self.client.close()
        if self.type == 'SSH':
            self.logger.info('ssh连接关闭成功：host=%s port=%s' % (self.ip, self.port))
        elif self.type == 'COM':
            if not self.client.isOpen():
                self.logger.info('com连接关闭成功：host=%s port=%s' % (self.ip, self.port))
            else:
                self.logger.error('com连接关闭成功：host=%s port=%s' % (self.ip, self.port))

    def send_cmd(self, cmd):
        if self.type == 'SSH':
            stdin, stdout, stderr = self.client.exec_command(cmd)
            stdin, stdout, stderr = stdin, stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
            self.logger.info('ssh命令发送成功:\n cmd=%s\n stdout=%s\n stderr=%s\n' % (
                cmd, stdout, stderr))
            return stdout, stderr
        elif self.type == 'COM':
            self.client.write(cmd.encode('utf-8'))
            self.client.write('\r'.encode('utf-8'))
            read = self.client.read_until('hkzy-ast2600:~#', 10240)
            self.logger.info('com命令发送成功:\n cmd=%s\n stdout=%s\n' % (cmd, read))

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

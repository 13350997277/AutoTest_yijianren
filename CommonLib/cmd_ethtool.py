from CommonLib.BaseCmd import *
from CommonLib.Logger import *


class ethtool(Base_Cmd):
    def __init__(self):
        super().__init__()
        self.cmd_head = 'ethtool'
        self.dev_name = 'dev_name'
        self.logger = MyLogger().logger

    def cmd_makeup(self, **option_args):
        retcode, retstr = -1, ''
        if self.dev_name not in option_args.keys():
            self.logger.error('cmd %s: 参数传入有误，未传入%s' % (self.cmd_head, self.dev_name))
            return retcode, retstr
        else:
            cmd = self.cmd_head + ' ' + option_args.get(self.dev_name)
            option_args.pop(self.dev_name)
            for key, value in option_args.items():
                try:
                    if getattr(self, key) == key:
                        cmd += ' -' + key + ' ' + value
                except Exception as e:
                    print(e)
                    return retcode, retstr
            return 0, cmd

    def handle_ret(self, stdout, stderr, **option_args):
        retcode, retstr = -1, ''
        if self.dev_name not in option_args.keys():
            self.logger.error('命令 %s: 参数传入有误，未传入%s' % (self.cmd_head, self.dev_name))
            return retcode, retstr
        elif len(option_args.keys()) == 1:
            return self.get_dev_info(stdout, stderr)
        else:
            return retcode, retstr

    def get_dev_info(self, stdout, stderr):
        retcode, retstr = -1, ''
        if 'No such device' in stderr:
            self.logger.error('获取网卡设备信息失败')
            return retcode, retstr
        else:
            self.logger.info('获取网卡设备信息成功')
            retcode = 0
            return retcode, retstr

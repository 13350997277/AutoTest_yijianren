from CommonLib.BaseCmd import *


class ethtool(Base_Cmd):
    def __init__(self):
        super().__init__()
        self.cmd_head = 'ethtool'
        self.DEVNAME = 'DEVNAME'

    def cmd_makeup(self, **option_args):
        retcode, retstr = -1, ''
        if self.DEVNAME not in option_args.keys():
            print('cmd %s: 参数传入有误，未传入%s' % (self.cmd_head, self.DEVNAME))
            return retcode, retstr
        else:
            cmd = self.cmd_head + ' ' + option_args.get(self.DEVNAME)
            option_args.pop(self.DEVNAME)
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
        if self.DEVNAME not in option_args.keys():
            print('cmd %s: 参数传入有误，未传入%s' % (self.cmd_head, self.DEVNAME))
            return retcode, retstr
        elif len(option_args.keys()) == 1:
            return self.get_dev_info(stdout, stderr)
        else:
            return retcode, retstr

    def get_dev_info(self, stdout, stderr):
        retcode, retstr = -1, ''
        if 'No such device' in stderr:
            print('获取设备信息失败')
            return retcode, retstr
        else:
            print('获取设备信息成功')
            retcode = 0
            return retcode, retstr

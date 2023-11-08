from CommonLib.BaseCmd import *
from CommonLib.Logger import *


class reboot(Base_Cmd):
    def __init__(self):
        super().__init__()
        self.cmd_head = 'reboot'
        self.logger = logger.logger

    def cmd_makeup(self, **option_args):
        retcode, retstr = -1, ''
        cmd = self.cmd_head
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
        if stderr:
            self.logger.error('reboot失败')
        else:
            self.logger.info('reboot成功')
            retcode = 0
        return retcode, retstr

class Base_Cmd():
    def __init__(self):
        self.cmd_head = ''
        self.cmd_unavailable_ret = 'command not found'

    def cmd_makeup(self, **option_args):
        pass

    def cmd_check_available(self, stdout, stderr):
        if self.cmd_unavailable_ret in stdout or self.cmd_unavailable_ret in stderr:
            return False
        else:
            return True

    def handle_ret(self, stdout, stderr, **option_args):
        pass

import logging
from logging.handlers import RotatingFileHandler
import time
import os


class MyLogger:
    def __init__(self):
        start_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))
        self.log_path = '..\..\TestLog\%s_%s.log' % (os.path.basename(os.getcwd()), start_time)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)')
        fh = RotatingFileHandler(self.log_path, maxBytes=1024 * 1024 * 1000, backupCount=5, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)


logger = MyLogger()

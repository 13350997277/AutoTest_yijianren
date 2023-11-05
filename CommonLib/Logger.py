import logging
from logging.handlers import RotatingFileHandler
from conftest import *
import time


class MyLogger:
    def __init__(self):
        self.log_path = pytest_configure().get('log_path')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)')
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)')
        fh = RotatingFileHandler(self.log_path, maxBytes=1024 * 1024 * 10, backupCount=5, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)

        self.logger.handlers = [self.logger.handlers[0]]  # 解决日志重复输出问题
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

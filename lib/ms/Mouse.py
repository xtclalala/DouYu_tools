# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/6  14:28
import re
import pyautogui

from lib.log.log_util import logging
from lib.items.singleton import Singleton
from lib.config.config_util import ConfigUtil
class Mouse(metaclass=Singleton):

    def __init__(self):
        self.mouse = pyautogui
        self.mouse.PAUSE = 1
        conf = ConfigUtil()
        self.msg_rule = conf.msg_rule
        self.true_False()

    def true_False(self):
        if self.mouse.size().width != 1920 or self.mouse.size().height != 1080:
            logging.warning("not 1080p")

    def get_msg(self, msg_dict):
        msg = msg_dict.get("txt")
        msg_type = msg_dict.get("type")
        msg_rule = self.msg_rule.get(msg_type)
        msg_width, msg_height = re.match(msg_rule, msg).groups()
        self.run_mouse(msg_width, msg_height)

    def run_mouse(self, x, y):
        self.mouse.click(self.width_x(x), self.height_y(y))

    @staticmethod
    def width_x(x):
        if int(x) > 20:
            logging.warning(f"{x} is too big")
        return 96 * (int(x) - 1) + 48

    @staticmethod
    def height_y(y):
        if ord(y) - 96 > 12:
            logging.warning(f"{y} is too big")
        return 90 * (ord(y) - 97) + 45

if __name__ == '__main__':
    m = Mouse()
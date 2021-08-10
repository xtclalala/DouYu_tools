# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/6  11:20
import re

from lib.items.singleton import Singleton
from lib.config.config_util import ConfigUtil
from lib.log.log_util import logging


class Cheek(metaclass=Singleton):

    def __init__(self):
        conf = ConfigUtil()
        self.type_ = conf.type_

    def cheek_msg(self, msg_dict):
        if not isinstance(msg_dict, dict):
            logging.error("msg_dict is not dict")
            return False, 0

        msg = msg_dict.get("txt", False)

        if msg is False:
            logging.error("do not have msg")
            return False, 0
        msg = msg.lower().strip()
        for key, value in self.type_:

            re_ = re.match(value, msg)
            if re_:
                return True, key
        return False, 0

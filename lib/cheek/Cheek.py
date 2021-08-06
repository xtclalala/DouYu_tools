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
        self.rule_dict = conf.msg_rule

    def cheek_msg(self, msg_dict):
        if not isinstance(msg_dict, dict):
            logging.error("msg_dict is not dict")
            return False

        msg = msg_dict.get("txt", False)

        if msg is False:
            logging.error("do not have msg")
            return False
        msg_type_ = msg_dict.get("type", "chatmsg")
        msg_rule = self.rule_dict.get(msg_type_)

        msg = msg.lower().strip()
        re_ = re.match(msg_rule, msg)
        if re_:
            return True
        else:
            return False

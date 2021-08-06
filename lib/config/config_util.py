# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  14:42
import re

from lib.items.singleton import Singleton
from lib.items.config_base import RawConfig
from base import get_path


class ConfigUtil(metaclass=Singleton):
    def __init__(self):
        config = RawConfig(get_path())

        self.room_id = config.get("socket", "room_id")
        self.heartbeat_interval = int(config.get("socket", "heartbeat_interval"))
        self.host = config.get("socket", "host")
        self.port = int(config.get("socket", "port"))
        self.msg_rule = config.get_dict("msg_rule")

    def get_msg_type(self):
        return list(self.msg_rule.keys())


if __name__ == '__main__':
    c = ConfigUtil()
    print(re.match("^([0-9]{1,2})([a-z])$", "11b").groups())
    print(ord("a"))

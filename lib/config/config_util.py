# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  14:42
import sys
import os

if os.path.realpath(__file__) not in sys.path:
    sys.path.insert(0, os.path.realpath(__file__).split("\\lib\\")[0])

from lib.items.singleton import Singleton
from lib.items.config_base import RawConfig
from base import get_path

class ConfigUtil(metaclass=Singleton):
    def __init__(self):
        config = RawConfig(get_path())
        # 进行读操作
        self.host = config.get("root", "host")
        self.port = config.get("root", "port")


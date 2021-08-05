# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  15:36
import logging
from configparser import RawConfigParser

from lib.log.log_util import logging


class RawConfig(object):

    def __init__(self, path=None):
        if path is None:
            raise logging.info("RawConfig not have path")
        self.app_config = RawConfigParser()
        try:
            self.app_config.read(path)
        except Exception as e:
            logging.error("RawConfig path is mistake")

    def get_dict(self, section):
        """
        选择 section 的内容，将其转变成字典形式
        Args:
            section: str 配置文件的部分内容

        Returns:
            以字典形式返回选择的内容
        """
        if isinstance(section, str):
            try:
                config_dict = dict(self.app_config[section])
            except Exception as e:
                print(e)
                config_dict = None
            return config_dict
        else:
            raise TypeError(f"'{section}' is not str")

    def get(self, section, option):
        """
        得到config文件的指定内容
        Args:
            section: str 配置文件的部分内容
            option: str 部分内容的其中一个选项

        Returns:

        """
        if isinstance(section, str) is None:
            raise TypeError(f"'{section}' is not str")
        if isinstance(option, str) is None:
            raise TypeError(f"'{option}' is not str")
        try:
            number = self.app_config.get(section, option)
        except Exception as e:
            print(e)
            number = None
        return number

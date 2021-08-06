# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  15:37
import os


def get_path():
    path, filename = os.path.split(os.path.realpath(__file__))
    return path + "\config.conf"

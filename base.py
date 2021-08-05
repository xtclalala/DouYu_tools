# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  15:37

import os

def get_path():
    path, filename = os.path.split(os.path.realpath(__file__))
    return path


def wai(data):
    def n():
        m = data() + 4
        return m
    return n

@wai
def add():
    c = 3
    return c

print(add())



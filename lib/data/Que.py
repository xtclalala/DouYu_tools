# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/6  10:40
import queue

from threading import Thread
from lib.cheek.Cheek import Cheek
from lib.ms.Mouse import Mouse


class Que(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.que = queue.Queue()

    def put(self, item):
        # item = {"name": 用户名称, "txt": 弹幕内容, "type": 弹幕类型}
        if Cheek().cheek_msg(item):
            self.que.put(item)

    def run(self):
        while True:
            Mouse().get_msg(self.que.get())

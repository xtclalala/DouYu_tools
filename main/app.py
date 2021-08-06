# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/6  9:17
import sys
import os

if os.path.realpath(__file__) not in sys.path:
    sys.path.insert(0, os.path.realpath(__file__).split("\\main\\")[0])
# print(sys.path)

from lib.sock.DouYu import DouYu
from lib.config.config_util import ConfigUtil
from lib.data.Que import Que


class APP(object):

    def __init__(self):
        config = ConfigUtil()
        room_id = config.room_id
        heartbeat_interval = config.heartbeat_interval
        host = config.host
        port = config.port
        self.dou_yu = DouYu(room_id=room_id,
                            heartbeat_interval=heartbeat_interval,
                            barrage_host=host,
                            barrage_port=port)
        self.msg_type_list = config.get_msg_type()
        self.que = Que()

    def run(self):
        for type_ in self.msg_type_list:
            self.dou_yu.add_handler(type_, self.payload_handler)
        self.dou_yu.start()
        self.get_msg_from_que()

    def payload_handler(self, msg, type_):
        output = {"name": msg['nn'], "txt": msg['txt'], "type": type_}
        print(output)
        self.que.put(output)
    # todo 取队列数据, 控制鼠标点击位置

    def get_msg_from_que(self):
        self.que.start()


if __name__ == '__main__':
    a = APP()
    a.run()
